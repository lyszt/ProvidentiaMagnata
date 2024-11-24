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


def create_or_update_message_details(message_details: dict):
    logging.info(f"[ Processing message from user at Guild: {message_details['guild_id']} ]")

    # Ensure the user profile exists
    user_profile = Profiles.get_or_none(userid=message_details['user_id'])
    if not user_profile:
        logging.error(f"User profile not found for ID: {message_details.get('user_id')}")
        return


    # Unpack message details
    message_text = message_details.get('message_text')
    sentiment_score = message_details.get('sentiment_score')
    subjectivity = message_details.get('subjectivity')
    timestamp = message_details.get('timestamp')
    guild_id = message_details.get('guild_id')
    channel_id = message_details.get('channel_id')
    topic = message_details.get('topic')
    message_id = message_details.get('message_id')

    # Create or update message
    try:
        with db.atomic():
            past_messages = (
                Messages
                .select()
                .where(Messages.user == user_profile)
            )
            sentiments = [message.sentiment_score for message in past_messages]
            average_sentiment = statistics.mean(sentiments) if sentiments else 0
            Profiles.update({Profiles.sentiment_score: average_sentiment}).where(
                Profiles.userid == message_details['user_id']
            ).execute()

            message_record, created = Messages.get_or_create(
                timestamp=timestamp,
                user=user_profile,
                channel_id=channel_id,
                guild_id=guild_id,
                defaults={
                    'message_text': message_text,
                    'sentiment_score': sentiment_score,
                    'subjectivity': subjectivity,
                }
            )
            if not created:
                message_record.message_text = message_text
                message_record.sentiment_score = sentiment_score
                message_record.subjectivity = subjectivity
                message_record.save()
                logging.info(f"Updated message for user.")
            else:
                logging.info(f"Created new message for user.")

            topic_record, created = MessageTopics.get_or_create(
                message=message_record,
                defaults={
                    'topic_name': f"{topic}",
                    'message_id': message_id,
                }
            )
            if not created:
                topic_record.message_id = message_id
                topic_record.save()
                logging.info(f"Updated topic for message.")
            else:
                logging.info(f"Created message topic for analysis.")
    except Exception as e:
        logging.error(f"Error while creating/updating message record: {e}")


class UserCollect:
    def __init__(self):
        pass

