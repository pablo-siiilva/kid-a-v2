import time

CHANNEL_ID_ORIGINAL = 1246881463266181171  # ID for #one-word-each
CHANNEL_ID_DESTINATION = 1256777917468381246  # ID for the finished sentences channel
CHANNEL_ID_DESTINATION_RANDOM = 1243270048295026811  # ID for general chat

words = []


def form_sentence():
    return ' '.join(words)


async def fetch_message_history(channel):
    print("Fetching message history...")
    try:
        async for message in channel.history(limit=100):  # Ajustar o limite conforme necessário
            if message.author.bot:
                continue
            if message.content.endswith(('.', '!', '?')):
                break
            words.append(message.content)
        words.reverse()
        print("Finished fetching message history.")
    except Exception as e:
        print(f"Error fetching message history: {e}")


async def initialize(client):
    print("INITIALIZING ONE-WORD-EACH MODULE")

    original_channel = client.get_channel(CHANNEL_ID_ORIGINAL)
    if original_channel is None:
        print(f"Failed to get channel with ID {CHANNEL_ID_ORIGINAL}")
        return
    await fetch_message_history(original_channel)
    print(f"Fetched messages: {words}")

    print("ONE-WORD-EACH MODULE INITIALIZED SUCCESSFULLY")


async def handleMessage(client, message):
    if message.channel.id == CHANNEL_ID_ORIGINAL and not message.author.bot:
        print(f"New message in #{message.channel.name} by {message.author.name}: {message.content}")
        words.append(message.content)
        if message.content.endswith(('.', '!', '?')):
            destination_channel = client.get_channel(CHANNEL_ID_DESTINATION)
            if destination_channel is None:
                print(f"Failed to get destination channel with ID {CHANNEL_ID_DESTINATION}")
                return
            sentence = form_sentence()
            print(f"Sending sentence: {sentence}")
            await destination_channel.send(f"#one-word-each has just finished a new sentence.\n"
                                           f"<t:{int(time.time())}>: {sentence}")
            words.clear()