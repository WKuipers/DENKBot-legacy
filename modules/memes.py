import os
import json
import asyncio


class MemesModule:
    def __init__(self, client):
        try:
            self.memes = json.load(open('memes.json'))
        except FileNotFoundError:
            self.memes = {}
        self.delete = {}
        self.client = client
        self.client.event(self.on_message)

    def add_meme(self, message):
        try:
            key, value = message[9:].split('|')
        except ValueError:
            return ('Command not formatted correctly!\n'
                    'The correct syntax is !addmeme trigger|response')
        key = key.lower()
        if len(key) < 4:
            return 'That trigger is too small.'
        if len(key) > 64:
            return 'That trigger is too large.'
        if key not in self.memes:
            self.memes[key] = value


    def get_meme(self, message):
        hits = filter(lambda x: x in message.lower(), self.memes.keys())
        return '\n'.join(map(self.memes.get, hits))


    def delete_this(self, message):
        message = message[12:]
        if message not in self.memes:
            return 'One can not delete what is not there.'
        if message not in self.delete:
            self.delete[message] = 0
        self.delete[message] = self.delete[message] + 1
        if self.delete[message] >= 3:
            del self.delete[message]
            del self.memes[message]
            return 'Deleted ' + message
        else:
            return ('There are now {} votes to delete {}'
                    .format(self.delete[message],message))


    async def store_memes(self):
        while True:
            await asyncio.sleep(5)
            with open('memes.json', 'w') as f:
                json.dump(self.memes, f)


    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        elif message.content.startswith('!addmeme '):
            response = self.add_meme(message.content)
        elif message.content.startswith('!deletethis '):
            response = self.delete_this(message.content)
        else:
            response = self.get_meme(message.content)

        if response:
            await self.client.send_message(message.channel, response)
