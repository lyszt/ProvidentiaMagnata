from peewee import Model, CharField, SqliteDatabase, DateTimeField, BooleanField, TextField, IntegerField, \
    ForeignKeyField

db = SqliteDatabase("/home/aluno/PycharmProjects/ProvidentiaMagnata/Bot/Data/users.db")

# USER PROFILING

class Profiles(Model):
    username = CharField(unique=True)  # Discord username (e.g., 'username#1234')
    userid = CharField(unique=True)  # Unique Discord user ID
    discriminator = CharField()  # The 4-digit discriminator (e.g., '1234')
    avatar_url = CharField(null=True)  # Avatar URL (if available)
    status = CharField(default="offline")  # User's current status: 'online', 'offline', 'idle', 'dnd'
    last_seen = DateTimeField(null=True)  # Timestamp of the last time the user interacted
    joined_at = DateTimeField(null=True)  # Timestamp of when the user joined
    is_bot = BooleanField(default=False)  # Whether the user is a bot
    bio = TextField(null=True)  # Optional user bio or interests
    sentiment_score = IntegerField(default=0)  # Overall sentiment score for the user
    last_interaction = DateTimeField(null=True)  # Last time the user interacted
    created_at = DateTimeField()  # When the profile was created

    class Meta:
        database = db


class Messages(Model):
    user = ForeignKeyField(Profiles, backref='messages')  # Link to the Profiles table
    message_text = TextField()  # The content of the message
    timestamp = DateTimeField()  # Timestamp of when the message was sent
    sentiment_score = IntegerField(null=True)  # Sentiment score for the message
    message_type = CharField(default='text')  # Type of message (e.g., text, image, link)
    channel_id = CharField(null=True)  # The channel the message was sent in (optional)

    class Meta:
        database = db  # Specify the database connection to use

class MessageTopics(Model):
    message = ForeignKeyField(Messages, backref='topics')
    topic_name = CharField()  # Topic, e.g., 'music', 'gaming', 'tech', etc.
    relevance_score = IntegerField()  # A score indicating how relevant this topic is to the message

    class Meta:
        database = db  # Specify the database connection to use

class UserActivity(Model):
    user = ForeignKeyField(Profiles, backref='activities')
    activity_type = CharField()  # e.g., 'sent_message', 'liked_message', etc.
    count = IntegerField(default=0)  # Count of occurrences of this activity type
    timestamp = DateTimeField()
    class Meta:
        database = db  # Specify the database connection to use


class UserPreferences(Model):
    user = ForeignKeyField(Profiles, backref='preferences')
    preference_name = CharField()  # E.g., 'favorite_game', 'preferred_language'
    preference_value = TextField()  # E.g., 'Minecraft', 'Python'

    class Meta:
        database = db  # Specify the database connection to use


# =======================================================================

#  UTILS
class Whitelist(Model):
    userid = CharField(unique=True)

    class Meta:
        database = db
