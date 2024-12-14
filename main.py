from datetime import datetime

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

deleted_messages = []

@client.event
async def on_ready():
    await log(f'[MAIN] Bot connected as {client.user}')
    try:

        await client.get_channel(CHANNEL_GENERAL).send("Hello fuckers >:)")

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
            if message.channel.id == ONE_WORD_EACH_CHANNEL:
                await one_word_each.handle_message(client, message)

            if message.content.startswith(".pairs"):
                await album_exchange_pairs.handle_message(client, message)

            if message.content.startswith(".deleted"):
                args = message.content.split()
                count = 1
                if len(args) > 1 and args[1].isdigit():
                    count = int(args[1])
                count = min(count, len(deleted_messages))

                if count > 0:
                    for deleted in deleted_messages[-count:]:
                        embed = discord.Embed(title="Deleted message", color=discord.Color.red())
                        embed.add_field(name="Author", value=deleted["author"], inline=False)
                        embed.add_field(name="Channel", value=deleted["channel"], inline=False)
                        embed.add_field(name="Timestamp", value=deleted["timestamp"], inline=False)
                        embed.add_field(name="Content", value=deleted["content"], inline=False)
                        if "media" in deleted:
                            embed.add_field(name="Media", value=deleted["media"], inline=False)
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Nenhuma mensagem apagada registrada.")

    except Exception as e:
        await log(f"[MAIN] Error in on_message: {e}")


@client.event
async def on_message_delete(message):
    if not message.author.bot:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            media_links = "\n".join([attachment.url for attachment in message.attachments])

            content = message.content if message.content else ""
            full_content = content if content else "[Empty message]"

            deleted_message_info = {
                "author": f"@{message.author} ({message.author.id})",
                "channel": f"#{message.channel} ({message.channel.id})",
                "timestamp": timestamp,
                "content": full_content
            }

            if media_links:
                deleted_message_info["media"] = media_links

            deleted_messages.append(deleted_message_info)
            if len(deleted_messages) > 10:
                deleted_messages.pop(0)

            await log(f"Mensagem apagada registrada: {deleted_message_info}")
        except Exception as e:
            await log(f"[MAIN] Erro em on_message_delete: {e}")


try:
    set_client(client)
    client.run(token)
except Exception as e:
    print(f"[MAIN] Error running the bot: {e}")
