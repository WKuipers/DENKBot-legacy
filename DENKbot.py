import discord
import asyncio
import os
import json

import memes

if 'DISCORD_TOKEN' in os.environ:
    token = os.environ['DISCORD_TOKEN']
else:
    print('No DISCORD_TOKEN environment variable defined, exiting')
    exit(1)
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)

memes.Mememodule(client)
client.run(token)
