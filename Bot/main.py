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

@client.event
async def on_ready():
    logging.info(f"Providence initialized at {datetime.now()}")
@client.event
async def on_message(message):
    if message.author == client.user:
        return


if __name__ == '__main__':
    Initialize().makeLogs()
    Initialize().makeTemp()
    Initialize().makeUser()
    logging.info("Logger initialized.")
    client.run(os.getenv('TOKEN'))

