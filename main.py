import discord
import dotenv

import one_word_each

config = dotenv.dotenv_values()
TOKEN = config.get("TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    try:
        await one_word_each.initialize(client)

    except Exception as e:
        print(f"Error in on_ready: {e}")


@client.event
async def on_connect():
    print("Bot is attempting to connect to Discord...")


@client.event
async def on_disconnect():
    print("Bot was disconnected from Discord.")


@client.event
async def on_error(event, *args, **kwargs):
    print(f"Error detected in event {event}: {args} - {kwargs}")


@client.event
async def on_message(message):
    try:
        await one_word_each.handleMessage(client, message)
    except Exception as e:
        print(f"Error in on_message: {e}")


print("Starting bot...")
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Error running the bot: {e}")
