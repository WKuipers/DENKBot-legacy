import discord
import asyncio
import os
import json


def add_meme(memes, message):
    try:
        key, value = message[9:].split('|')
    except ValueError:
        return ('Command not formatted correctly!\n'
                'The correct syntax is !addmeme trigger|response')
    if len(key) < 4:
        return 'That trigger is too small.'
    if len(key) > 64:
        return 'That trigger is too large.'
    if key not in memes:
        memes[key] = value


def get_meme(memes, message):
    return '\n'.join(map(memes.get,filter(lambda x: x in message, memes.keys())))


def delete_this(memes, message, delete):
    message = message[12:]
    if message not in memes:
        return 'One can not delete what is not there.'
    if message not in delete:
        delete[message] = 0
    delete[message] = delete[message] + 1
    if delete[message] >= 3:
        del delete[message]
        del memes[message]
        return 'Deleted ' + message
    else:
        return 'There are now {} votes to delete {}'.format(delete[message],message)

async def store_memes(memes):
    while True:
        await asyncio.sleep(3600)
        with open('memes.json', 'w') as f:
            json.dump(memes, f)


if 'DISCORD_TOKEN' in os.environ:
    token = os.environ['DISCORD_TOKEN']
else:
    print('No DISCORD_TOKEN environment variable defined, exiting')
    exit(1)
try:
    memes = json.load(open('memes.json'))
except FileNotFoundError:
    memes = {}
delete = {}
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    elif message.content.startswith('!addmeme '):
        response = add_meme(memes, message.content)
    elif message.content.startswith('!deletethis '):
        response = delete_this(memes, message.content, delete)
    else:
        response = get_meme(memes, message.content)

    if response:
        await client.send_message(message.channel, response)

loop = asyncio.get_event_loop()
loop.create_task(store_memes(memes))
client.run(token)
