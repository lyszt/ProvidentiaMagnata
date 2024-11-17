# Application Imports

import discord

# Util Imports
import logging
import datetime

# Running imports
import os
from dotenv import load_dotenv

# Modules
from Modules.configuration import *

# GLOBALS
ENV = "Config/providence.env"
load_dotenv(ENV)
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f"Providence initialized at {datetime.datetime.now()}")
@client.event
async def on_message(message):
    if message.author == client.user:
        return


if __name__ == '__main__':
    Initialize().makeLogs()
    logging.info("Logger initialized.")
    client.run(os.getenv('TOKEN'))
