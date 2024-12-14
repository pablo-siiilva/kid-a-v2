# Kid A

Code for the Kid A discord bot.

This bot is mainly focused on extra features for a discord server i have with some friends called Music Circlejerk X (yes it is a silly server).

## Environment setup

I run this code with Python3 with two extra modules:

```
pip install discord 
pip install python-dotenv
```

Then to set up the environment variables you just put a file named `.env` on the same directory as the main script with the following data:
```
TOKEN=[discord client token]
```

## Features

- Support for #one-word-each
- Command for pairing people on events such as album exchange:
  - `.pairs [name1] [name2] [etc...]` 
- Command for recovering deleted messages (max 10 messages, if no argument is provided then it'll only recover one message)
  - `.deleted [opt=number_of_messages]` 