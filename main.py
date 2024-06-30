import discord
import time

import dotenv

config = dotenv.dotenv_values()
TOKEN = config.get("TOKEN")
CHANNEL_ID_ORIGINAL = 1246881463266181171  # ID for #one-word-each
CHANNEL_ID_DESTINATION = 1256777917468381246  # ID for the finished sentences channel
CHANNEL_ID_DESTINATION_RANDOM = 1243270048295026811  # ID for general chat... originally i wanted it to print it there at random times of day lol

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# List to store the words
words = []


# Function to form a sentence from words
def form_sentence():
    return ' '.join(words)


async def fetch_message_history(channel):
    async for message in channel.history(limit=100):  # Adjust limit as needed
        if message.author.bot:
            continue
        if message.content.endswith(('.', '!', '?')):
            break
        words.append(message.content)
    words.reverse()


@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    original_channel = client.get_channel(CHANNEL_ID_ORIGINAL)
    await fetch_message_history(original_channel)
    print(f"Fetched messages: {words}")


@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID_ORIGINAL and not message.author.bot:
        print(f"New message in #{message.channel.name} by {message.author.name}: {message.content}")
        words.append(message.content)
        if message.content.endswith(('.', '!', '?')):  # Check if the sentence is complete
            destination_channel = client.get_channel(CHANNEL_ID_DESTINATION)
            sentence = form_sentence()
            print(f"Sending sentence: {sentence}")
            await destination_channel.send(f"#one-word-each has just finished a new sentence.\n"
                                           f"<t:{int(time.time())}>: {sentence}")
            words.clear()


client.run(TOKEN)
