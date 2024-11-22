import logging
from datetime import datetime
from .database_models import *


def create_or_update_user_profile(user_data: dict):
    logging.info(f"[ Analyzing message of civilizan n°{user_data.get('discriminator')} ]")
    db = SqliteDatabase("/home/aluno/PycharmProjects/ProvidentiaMagnata/Bot/Data/users.db")
    db.connect()
    # Unpack user data from the dictionary
    user_id = user_data.get('user_id')
    username = user_data.get('username')
    discriminator = user_data.get('discriminator')
    avatar_url = user_data.get('avatar_url')
    user_status = user_data.get('user_status')
    last_seen = user_data.get('last_seen')
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
        'last_interaction': None,
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
    db.close()

def create_or_update_message_details(message_details: dict):
    logging.info(f"[ Processing message from user: {message_details['user'].username}, Guild: {message_details['guild_id']} ]")
    db = SqliteDatabase("/home/aluno/PycharmProjects/ProvidentiaMagnata/Bot/Data/users.db")
    db.connect()

    # Unpack message details from the dictionary
    user_profile = message_details.get('user')
    message_text = message_details.get('message_text')
    sentiment_score = message_details.get('sentiment_score')
    subjectivity = message_details.get('subjectivity')
    timestamp = message_details.get('timestamp')
    guild_id = message_details.get('guild_id')
    channel_id = message_details.get('channel_id')

    # Create or update message record in the database
    message_record, created = Messages.get_or_create(
        timestamp=timestamp,
        guild_id=guild_id,
        channel_id=channel_id,
        user=user_profile,  # Assuming foreign key relationship
        defaults={
            'message_text': message_text,
            'sentiment_score': sentiment_score,
            'subjectivity': subjectivity,
            'created_at': datetime.now(),
        }
    )

    # Update message fields if the message already exists (not created)
    if not created:
        message_record.message_text = message_text
        message_record.sentiment_score = sentiment_score
        message_record.subjectivity = subjectivity
        message_record.save()

    db.close()
class UserCollect:
    def __init__(self):
        pass

