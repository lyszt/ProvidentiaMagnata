from peewee import Model, CharField, SqliteDatabase, DateTimeField, BooleanField, TextField, IntegerField, \
    ForeignKeyField, FloatField

db = SqliteDatabase("C:\\Users\\neoka\PycharmProjects\\ProvidentiaMagnata\Bot\Data\\users.db")

# USER PROFILING

class Profiles(Model):
    username = CharField(unique=True)
    userid = CharField(unique=True)
    discriminator = CharField()
    avatar_url = CharField(null=True)
    status = CharField(default="offline")
    last_seen = DateTimeField(null=True)
    joined_at = DateTimeField(null=True)
    is_bot = BooleanField(default=False)
    bio = TextField(null=True)
    sentiment_score = IntegerField(default=0)
    threat_level = IntegerField(default=0)
    last_interaction = DateTimeField(null=True)
    created_at = DateTimeField()

    class Meta:
        database = db


class Messages(Model):
    user = ForeignKeyField(Profiles, backref='messages')  # Links to Profiles
    message_id = CharField(unique=True)  # Unique Discord message ID
    message_text = TextField()
    timestamp = DateTimeField()
    sentiment_score = FloatField(null=True)
    subjectivity = FloatField(null=True)
    message_type = CharField(default='text')
    channel_id = CharField(null=True)
    guild_id = CharField(null=True)

    class Meta:
        database = db


class MessageTopics(Model):
    message = ForeignKeyField(Messages, backref='topics')  # Link to Messages
    topic_name = CharField(null=True)  # Topic name (e.g., 'music', 'gaming')

    class Meta:
        database = db


class UserActivity(Model):
    user = ForeignKeyField(Profiles, backref='activities')
    activity_type = CharField()  # Type of activity (e.g., 'sent_message', etc.)
    count = IntegerField(default=0)
    timestamp = DateTimeField()

    class Meta:
        database = db

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
