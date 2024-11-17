# Application Imports
import discord
# Util Imports
import logging
# Running imports
import os
from dotenv import load_dotenv


# GLOBALS
ENV = "Config/providence.env"
load_dotenv(ENV)
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Initialized as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(os.getenv('DISCORD_TOKEN'))
