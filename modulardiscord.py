import discord
import asyncio

import modules.memes as memes

class ModularDiscordClient():
   
    def __init__(self):
        self.client = discord.Client()
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.modules = {}


    def register_module(self, module, server):
        if str(server) not in self.modules:
            self.modules[str(server)] = [module]
        else:
            self.modules[str(server)].append(module)
        for event in module.events:
            self.client.loop.create_task(event())
    
    
    def module_loaded(self, module_name, server):
        if str(server) not in self.modules:
            return False
        for module in self.modules[str(server)]:
            if module.name == module_name:
                return True
        return False

    def register(self, message):
        module_name = message.content[10:]
        if (
                module_name == 'Memes'
                and not self.module_loaded(module_name, message.server)
            ):
            module = memes.MemesModule(self.client, message.server)
            self.register_module(module, message.server)

    async def on_ready(self):
        print('Logged in as ' + self.client.user.name)


    async def on_message(self, message):
        if message.content.startswith('!register'):
            self.register(message)
            return
        if str(message.server) not in self.modules:
            return
        for module in self.modules.get(str(message.server)):
            self.client.loop.create_task(module.on_message(message))
            

    def run(self, token):
        self.client.run(token)
