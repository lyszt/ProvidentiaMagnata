# Application Imports
import glob

import discord

# Databases

# Util Imports
import atexit

# Running imports
from dotenv import load_dotenv

# Modules
from Modules.configuration import *
from Modules.Data.collection import *
from Modules.Data.message_analysis import *
# GLOBALS
ENV = "Config/providence.env"
GLOBAL_MEMORY = "Data/global.db"
USER_DATA = "Data/users.db"
load_dotenv(ENV)
intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)
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


@client.event
async def on_ready():
    logging.info(f"Providence initialized at {datetime.now()}")
@client.event
async def on_message(interaction):
    if interaction.author == client.user:
        return
    if(interaction.author.bot):
        return

    # Lygon e Grão-Ducado Czéliano
    if interaction.guild.id == 704066892972949504 or interaction.guild.id == 696830110493573190:
        # Extract relevant user detailsS
        user_details = {
            'user_id': str(interaction.author.id),  # Unique Discord user ID
            'username': interaction.author.name,  # Discord username (e.g., 'username')
            'discriminator': interaction.author.discriminator,  # 4-digit discriminator (e.g., '1234')
            'avatar_url': str(interaction.author.avatar) if interaction.author.avatar else None,
            # Avatar URL (if available)
            'user_status': str(interaction.author.status),  # User's current status: 'online', 'offline', 'idle', 'dnd'
            'last_seen': interaction.author.activity.start if interaction.author.activity else None,
            # Last activity timestamp, if any
            'joined_at': interaction.author.created_at,  # Timestamp of when the user joined
            'is_bot': interaction.author.bot,  # Whether the user is a bot
            'bio': None  # No bio data is directly available from Discord API
        }
        create_or_update_user_profile(user_details)



@atexit.register
def killDatabases():
    logging.info("Killing databases...")
    for db_file in glob.glob("Bot/Data/**/*.db", recursive=True):
        db = SqliteDatabase(db_file)
        if not db.is_closed():
            db.close()
            logging.info(f"Closed database: {db_file}")




if __name__ == '__main__':
    Initialize().makeLogs()
    Initialize().makeTemp()
    Initialize().makeUser()
    logging.info("Logger initialized.")
    client.run(os.getenv('TOKEN'))

