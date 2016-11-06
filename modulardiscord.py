import discord
from importlib import import_module


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

    def register(self, module_name, server):
        if not self.module_loaded(module_name, server):
            module_path = '.'.join(['modules', module_name])
            try:
                module_class = import_module(module_path).module
                module = module_class(self.client, server)
                self.register_module(module, server)
                return module_name
            except ImportError:
                return None

    async def on_ready(self):
        print('Logged in as ' + self.client.user.name)
        for line in open('defaultmodules.txt').readlines():
            for server in self.client.servers:
                self.register(line.strip(), server)

    async def on_message(self, message):
        if message.content.startswith('!register'):
            module = self.register(message.content[10:], message.server)
            if module is None:
                await self.client.send_message(message.channel,
                                               'Failed to import module')
                return
        if str(message.server) not in self.modules:
            return
        for module in self.modules.get(str(message.server)):
            self.client.loop.create_task(module.on_message(message))

    def run(self, token):
        self.client.run(token)
