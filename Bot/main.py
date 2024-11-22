# Application Imports

import discord
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import tasks

# Databases
import peewee
from peewee import Model, CharField, SqliteDatabase
import sqlite3

# Util Imports
import logging
from datetime import datetime

# Running imports
import os
from dotenv import load_dotenv

# Modules
from Modules.configuration import *
from Modules.Data.collection import *
# GLOBALS
ENV = "Config/providence.env"
GLOBAL_MEMORY = "Data/global.db"
USER_DATA = "Data/users.db"
load_dotenv(ENV)
intents = discord.Intents.default()
intents.message_content = True

Databases = {
    "DB_global": SqliteDatabase("Data/global.db"),
    "config" : SqliteDatabase("Data/config.db")
}


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
    if(interaction.user.bot):
        return
    if(interaction.channel.id == 704066892972949504):
        # Extract relevant user detailsS
        user_details = {
            'user_id': str(interaction.author.id),  # Unique Discord user ID
            'username': interaction.author.name,  # Discord username (e.g., 'username')
            'discriminator': interaction.author.discriminator,  # 4-digit discriminator (e.g., '1234')
            'avatar_url': str(interaction.author.avatar_url) if interaction.author.avatar else None,
            # Avatar URL (if available)
            'user_status': str(interaction.author.status),  # User's current status: 'online', 'offline', 'idle', 'dnd'
            'last_seen': interaction.author.activity.start if interaction.author.activity else None,
            # Last activity timestamp, if any
            'joined_at': interaction.author.created_at,  # Timestamp of when the user joined
            'is_bot': interaction.author.bot,  # Whether the user is a bot
            'bio': None  # No bio data is directly available from Discord API
        }
        UserCollect().create_or_update_user_profile(user_details)









if __name__ == '__main__':
    Initialize().makeLogs()
    Initialize().makeTemp()
    Initialize().makeUser()
    logging.info("Logger initialized.")
    client.run(os.getenv('TOKEN'))

