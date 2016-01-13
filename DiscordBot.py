import discord
import pickle
import random

def main():
    credentials = dict()
    with open("login","r") as f:
        for line in f:
            key,value = line.split(":")
            credentials[key] = value.rstrip("\n")
    client = discord.Client()
    client.login(credentials["email"],credentials["password"])

    try:
        responses = pickle.load( open("responses.p","rb"))
    except FileNotFoundError:
        responses = dict()

    @client.event
    def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith("!add:"):
            reply = add(message,responses)
        elif message.content.startswith("!del:"):
            reply = delete(message,responses)
        elif message.content.startswith("!roll:"):
            reply = roll(message)
        else:
            reply = respond(message,responses)
        if len(reply) > 0:
            client.send_message(message.channel,reply)
        return

    @client.event
    def on_ready():
        print("Logged in as")
        print(client.user.name)
    
    client.run()

def add(message,responses):
    try:
        key,value = message.content[5:].split(":",maxsplit=1)
    except ValueError:
        return
    responses[key] = value
    pickle.dump(responses, open("responses.p","wb"))
    return "Response added!"

def delete(message,responses):
    key = message.content[5:]
    if key in responses:
        del responses[key]
    pickle.dump(responses, open("responses.p","wb"))
    return "Response deleted!"

def respond(message,responses):
    reply = []
    words = set(message.content.split())
    map(str.lower,words)
    match = False
    for word in words:
        if word in responses:
            match = True
            reply.append(responses[word])
    if match:
        return "\n".join(reply)
    return ""

def roll(message):
    try:
        val = int(message.content[6:])
        upper_bound = int(message.content[6:])
        return str(random.randint(0,upper_bound))
    except ValueError:
        return ""

if __name__ == "__main__":
    main()
