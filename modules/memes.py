import json
import asyncio


class MemesModule:
    def __init__(self, client, server):
        self.name = 'Memes'
        self.client = client
        self.server = server
        try:
            fp = open('_'.join([str(self.server), 'memes.json']))
            self.memes = json.load(fp)
        except FileNotFoundError:
            self.memes = {}
        self.delete = {}
        self.events = [self.store_memes]

    def add_meme(self, message):
        try:
            key, value = message.content[9:].split('|')
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
        trigger = message.content
        hits = filter(lambda x: x in trigger.lower(), self.memes.keys())
        return '\n'.join(map(self.memes.get, hits))

    def delete_this(self, message):
        trigger = message.content[12:]
        if trigger not in self.memes:
            return 'One can not delete what is not there.'
        if trigger not in self.delete:
            self.delete[trigger] = set([message.author.id])
        else:
            self.delete[trigger].add(message.author.id)
        if len(self.delete[trigger]) >= 3:
            del self.delete[trigger]
            del self.memes[trigger]
            return 'Deleted ' + trigger
        else:
            return ('There are now {} votes to delete {}'
                    .format(len(self.delete[trigger]), trigger))

    async def store_memes(self):
        while True:
            await asyncio.sleep(360)
            with open('_'.join([str(self.server), 'memes.json']), 'w') as fp:
                json.dump(self.memes, fp)

    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        elif message.server != self.server:
            return
        elif message.content.startswith('!addmeme '):
            response = self.add_meme(message)
        elif message.content.startswith('!deletethis '):
            response = self.delete_this(message)
        else:
            response = self.get_meme(message)
        if response:
            await self.client.send_message(message.channel, response)


module = MemesModule
