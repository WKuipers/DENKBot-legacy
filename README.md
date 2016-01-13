# DiscordBot.py

DiscordBot.py is a simple Python 3 program to run a chatbot for the Discord chat service.

##Dependencies
You will need [Discord.py](https://github.com/Rapptz/discord.py), which you can install with

`pip install Discord.py`

##Installation
Make sure Discord.py is installed then clone this repository.
Change the credentials in examplelogin to the credentials of the bot, and rename the file to login.
In order to store responses the program will try to write to a file called `responses.p`

##Usage
Run DiscordBot.py. It will print a message when it has succesfully logged in.

##Commands
`!add:trigger:response` adds a word to the database, and what to respond with when someone uses that word.

`!del:trigger` deletes a trigger from the database.

`roll:n` generates a random number from 0 to n.

##Limitations
Triggers can only be words without spaces. 
Randoms use python's random module which may not be the best.
