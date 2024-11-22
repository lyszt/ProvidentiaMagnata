import datetime

from database_models import *

class UserCollect:
    def __init__(self):
        pass

    def create_or_update_user_profile(self, user_data: dict):
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
            'created_at': datetime.datetime.now(),
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
