# Application Imports
import glob
import typing

import translate
import discord
from discord import app_commands
from discord.ext import tasks, commands
from openai import OpenAI
# Databases

# Util Imports
import atexit
import random

# Running imports
from dotenv import load_dotenv

# Modules
from Modules.Utils import lists
from Modules.configuration import *
from Modules.Data.collection import *
from Modules.Data.message_analysis import *
from Modules.Speech.speech import *
# GLOBALS
ENV = "Config/providence.env"


load_dotenv(ENV)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
@client.event
async def on_ready():
    logging.info(f"Providence initialized at {datetime.now()}")
    await client.wait_until_ready()
    await tree.sync(guild=None)
    logging.info("Synced.")

    async def create_presence():
        target_channel = client.get_channel(704066892972949507)
        history = target_channel.history(limit=20)
        conversational_context = ""
        async for msg in history:
            conversational_context += f"{msg.author.name} diz: {msg.content}\n"
        presence_status = Language().genPresence(conversational_context).split('.')[0] + '.'
        logging.info(presence_status)
        try:
            await client.change_presence(
                status=discord.Status.dnd,
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=presence_status,
                    url="https://www.youtube.com/watch?v=1DwmADdc8EE"
                )
            )
        except Exception as e:
            logging.info("Could not change presence: ", e)

    @tasks.loop(minutes=10)
    async def change_presence_task():
        await create_presence()

    change_presence_task.start()




@client.event
async def on_message(interaction):
    if interaction.author == client.user:
        return
    if(interaction.author.bot):
        return
    # Lygon e Grão-Ducado Czéliano
    if interaction.guild.id == 704066892972949504 or interaction.guild.id == 696830110493573190:
        translator = translate.Translator(from_lang='pt', to_lang="en")
        message_text = translator.translate(interaction.content)

        user_profile = Profiles.get_or_none(userid = interaction.author.id)
        # Extract relevant user detailsS
        user_details = {
            'user_id': str(interaction.author.id),  # Unique Discord user ID
            'username': interaction.author.name,  # Discord username (e.g., 'username')
            'discriminator': interaction.author.discriminator,  # 4-digit discriminator (e.g., '1234')
            'avatar_url': str(interaction.author.avatar) if interaction.author.avatar else None,
            # Avatar URL (if available)
            'user_status': str(interaction.author.status),  # User's current status: 'online', 'offline', 'idle', 'dnd'
            'last_seen': interaction.author.activity.start if interaction.author.activity else None,
            'timestamp': interaction.created_at,
            # Last activity timestamp, if any
            'joined_at': interaction.author.joined_at,  # Timestamp of when the user joined
            'is_bot': interaction.author.bot,  # Whether the user is a bot
            'bio': None  # No bio data is directly available from Discord API
        }
        create_or_update_user_profile(user_details)
        message_analysis = analyse_message(message_text)
        # 10 messages per context for topic analysis
        history = interaction.channel.history(limit=5)
        conversational_context = "" + f"{interaction.author.name} diz: {interaction.content}"
        async for msg in history:
            conversational_context += f"{msg.author.name} diz: {msg.content}\n"
        topic = Language().findTopic(conversational_context)
        sentiment_score = message_analysis['sentiment_score']
        subjectivity = message_analysis['subjectivity']
        message_details = {
            'user': user_profile,
            'user_id': str(interaction.author.id),
            'message_text': interaction.content,
            'sentiment_score': sentiment_score,
            'subjectivity': subjectivity,
            'timestamp': interaction.created_at,
            'guild_id': interaction.guild.id,
            'message_id': interaction.id,
            'channel_id': interaction.channel.id,
            'topic': topic,
        }

        create_or_update_message_details(message_details)

@tree.command(name="ping")
async def ping(message: discord.Interaction):
    await message.response.send_message(f"Pong! ({client.latency*1000}ms)")

@tree.command(name="contact")
async def contact(interaction: discord.Interaction, message_input: str, voice: typing.Optional[bool] = False, image: typing.Optional[bool] = False):
    if interaction.user.id == 1047943536374464583:
        await Conversation().run(interaction, message_input, voice, image)


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
    client.run(os.getenv('DISCORD_TOKEN'))

