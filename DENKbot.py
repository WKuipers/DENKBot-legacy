#!/usr/bin/env python
import os
import modulardiscord as md

if 'DISCORD_TOKEN' in os.environ:
    token = os.environ['DISCORD_TOKEN']
else:
    print('No DISCORD_TOKEN environment variable defined, exiting')
    exit(1)
client = md.ModularDiscordClient()

client.run(token)
