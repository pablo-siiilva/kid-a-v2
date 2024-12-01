import time

from printutil import log

CHANNEL_ID_DESTINATION = 1256777917468381246  # ID for the finished sentences channel
CHANNEL_ID_DESTINATION_RANDOM = 1243270048295026811  # ID for general chat

words = []


def form_sentence():
    return ' '.join(words)


async def fetch_message_history(channel):
    await log("[ONE-WORD-EACH] Fetching message history...")
    try:
        async for message in channel.history(limit=100):
            if message.author.bot:
                continue
            if message.content.endswith(('.', '!', '?')):
                break
            words.append(message.content)
        words.reverse()
        await log(f"[ONE-WORD-EACH] Messages fetched: ${''.join(words)}")
    except Exception as e:
        await log(f"[ONE-WORD-EACH] Error fetching message history: {e}")


async def initialize(client, channel_id):
    await log("[ONE-WORD-EACH] INITIALIZING ONE-WORD-EACH MODULE")

    original_channel = client.get_channel(channel_id)
    if original_channel is None:
        await log(f"[ONE-WORD-EACH] Couldn't find channel {channel_id}")
        return
    await fetch_message_history(original_channel)

    await log("[ONE-WORD-EACH] ONE-WORD-EACH MODULE INITIALIZED SUCCESSFULLY")


async def handle_message(client, message):
    await log(f"[ONE-WORD-EACH] New message in #{message.channel.name} by {message.author.name}: {message.content}")
    words.append(message.content)
    if message.content.endswith(('.', '!', '?')):
        destination_channel = client.get_channel(CHANNEL_ID_DESTINATION)
        if destination_channel is None:
            await log(f"[ONE-WORD-EACH] Failed to get destination channel with ID {CHANNEL_ID_DESTINATION}")
            return
        sentence = form_sentence()
        await log(f"[ONE-WORD-EACH] Sending sentence: {sentence}")
        await destination_channel.send(f"#one-word-each has just finished a new sentence.\n"
                                       f"<t:{int(time.time())}>: {sentence}")
        words.clear()
