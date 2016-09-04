# DENKBot.py

DENKBot.py is a simple Python 3.5 program to run a chatbot for the Discord chat service.

##Dependencies
All dependencies are in the `requirements.txt` file

##Installation
Clone the repository
Ensure there is an environment variable called `DISCORD_TOKEN` containing your bot token
In order to store responses the program will try to write to a file called `memes.json`

##Usage
Run DENKBot.py. It will print a message when it has succesfully logged in.

##Commands
`!addmeme trigger|response` adds a word to the database, and what to respond with when someone uses that word.

##Issues
Triggers can not be deleted
It will attempt to find every key in every message which may be slow with lots of keys.
