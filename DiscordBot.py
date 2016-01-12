import discord
import pickle

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
            try:
                key,value = message.content[5:].split(":",maxsplit=1)
            except ValueError:
                return
            responses[key] = value
            pickle.dump(responses, open("responses.p","wb"))
            client.send_message(message.channel, "Goede meme toegevoegd!")
            return

        if message.content.startswith("!del:"):
            key = message.content[5:]
            if key in responses:
                del responses[key]
            pickle.dump(responses, open("responses.p","wb"))
            return

        reply = []
        words = set(message.content.split())
        map(str.lower,words)
        match = False
        for word in words:
            if word in responses:
                match = True
                reply.append(responses[word])
        if match:
            client.send_message(message.channel,"\n".join(reply))
        return

    @client.event
    def on_ready():
        print("Logged in as")
        print(client.user.name)
    
    client.run()

if __name__ == "__main__":
    main()
