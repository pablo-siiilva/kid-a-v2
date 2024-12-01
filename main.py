import discord
import os

import one_word_each
import album_exchange_pairs
import random_song_from_playlist
import bumpin_that

from printutil import log, set_client

token = os.getenv("TOKEN")
youtube_api_token = os.getenv("YOUTUBE_TOKEN")

ONE_WORD_EACH_CHANNEL = 1246881463266181171  # ID for #one-word-each
BUMP_CHANNEL = 1310459216707719189  # ID for #one-word-each

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

CHANNEL_GENERAL = 1243270048295026811

@client.event
async def on_ready():
    await log(f'[MAIN] Bot connected as {client.user}')
    try:

        await one_word_each.initialize(client, ONE_WORD_EACH_CHANNEL)
        await bumpin_that.initialize(client, BUMP_CHANNEL)
        await random_song_from_playlist.initialize(client, youtube_api_token)

    except Exception as e:
        await log(f"[MAIN] EXCEPTION: {e}")


@client.event
async def on_connect():
    await log("[MAIN] Attempting to connect to Discord...")


@client.event
async def on_disconnect():
    await log("[MAIN] I was disconnected from Discord! >:(")


@client.event
async def on_error(event, *args, **kwargs):
    await log(f"[MAIN] ERROR!!! {event}: {args} - {kwargs}")


@client.event
async def on_message(message):
    try:
        if not message.author.bot:
            # If message comes from the one-word-each channel
            if message.channel.id == ONE_WORD_EACH_CHANNEL:
                await one_word_each.handle_message(client, message)

            if message.content.startswith(".pairs"):
                await album_exchange_pairs.handle_message(client, message)
    except Exception as e:
        await log(f"[MAIN] Error in on_message: {e}")


try:
    set_client(client)
    client.run(token)
except Exception as e:
    print(f"[MAIN] Error running the bot: {e}")
