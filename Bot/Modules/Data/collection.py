import logging
from datetime import datetime
from profile import Profile

from .database_models import *
import statistics



def create_or_update_user_profile(user_data: dict):
    logging.info(f"[ Analyzing message of civilian n°{user_data.get('discriminator')} ]")
    # Unpack user data from the dictionary
    user_id = user_data.get('user_id')
    username = user_data.get('username')
    discriminator = user_data.get('discriminator')
    avatar_url = user_data.get('avatar_url')
    user_status = user_data.get('user_status')
    last_seen = user_data.get('last_seen')
    timestamp = user_data.get('timestamp')
    joined_at = user_data.get('joined_at')
    is_bot = user_data.get('is_bot')
    bio = user_data.get('bio')

    # Create or update user profile in the database
    user_profile, created = Profiles.get_or_create(userid=user_id, defaults={
        'username': username,
        'discriminator': discriminator,
        'avatar_url': avatar_url,
        'status': user_status,
        'last_seen': last_seen,
        'joined_at': joined_at,
        'is_bot': is_bot,
        'bio': bio,
        'sentiment_score': 0,
        'last_interaction': timestamp,
        'created_at': datetime.now(),
    })
    # Update profile fields if the profile already exists (not created)
    if not created:
        user_profile.username = username
        user_profile.discriminator = discriminator
        user_profile.avatar_url = avatar_url
        user_profile.status = user_status
        user_profile.last_seen = last_seen
        user_profile.joined_at = joined_at
        user_profile.is_bot = is_bot
        user_profile.bio = bio
        user_profile.save()


import logging
import statistics

import logging
import statistics


def create_or_update_message_details(message_details: dict):
    logging.info(f"[Processing message from user at Guild: {message_details['guild_id']}]")

    user_profile = Profiles.get_or_none(userid=message_details['user_id'])
    if not user_profile:
        logging.error(f"User profile not found for ID: {message_details.get('user_id')}")
        return

    message_text = message_details.get('message_text')
    sentiment_score = message_details.get('sentiment_score')
    subjectivity = message_details.get('subjectivity')
    timestamp = message_details.get('timestamp')
    guild_id = message_details.get('guild_id')
    channel_id = message_details.get('channel_id')
    topic = message_details.get('topic')
    message_id = message_details.get('message_id')

    try:
        with db.atomic():
            past_messages = Messages.select().where(Messages.user == user_profile)
            sentiments = [message.sentiment_score for message in past_messages]
            average_sentiment = statistics.mean(sentiments) if sentiments else 0

            Profiles.update({Profiles.sentiment_score: average_sentiment}).where(
                Profiles.userid == message_details['user_id']
            ).execute()

            message_record = Messages.get_or_none(message_id=message_id)

            if message_record:
                # If the message exists, update it
                message_record.message_text = message_text
                message_record.sentiment_score = sentiment_score
                message_record.subjectivity = subjectivity
                message_record.timestamp = timestamp
                message_record.channel_id = channel_id
                message_record.guild_id = guild_id
                message_record.save()
                logging.info(f"Updated message for user {user_profile.userid}.")
            else:
                # If the message doesn't exist, create a new record
                message_record = Messages.create(
                    message_id=message_id,
                    user=user_profile,
                    message_text=message_text,
                    sentiment_score=sentiment_score,
                    subjectivity=subjectivity,
                    timestamp=timestamp,
                    channel_id=channel_id,
                    guild_id=guild_id
                )
                logging.info(f"Created new message for user {user_profile.userid}.")

            # Save or update the topic
            topic_record, created = MessageTopics.get_or_create(
                message=message_record,  # This links to the Messages model via the ForeignKeyField
                defaults={
                    'topic_name': topic,
                    'message_id': message_id  # Save message_id in MessageTopics
                }
            )

            if not created:
                topic_record.topic_name = topic
                topic_record.save()
                logging.info(f"Updated topic for message {message_record.message_id}.")
            else:
                logging.info(f"Created new topic for message {message_record.message_id}.")


    except Exception as e:
        logging.error(f"Error while creating/updating message record: {e}")


class UserCollect:
    def __init__(self):
        pass

