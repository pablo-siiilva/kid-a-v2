import random

from printutil import log


async def handle_message(client, message):
    await log(f"[PAIRS] New pairs message in #{message.channel.name} by {message.author.name}: {message.content}")
    channel_id = message.channel.id
    arguments = message.content.split(" ")
    arguments.pop(0)
    random.shuffle(arguments)
    pairs = [(arguments[i], arguments[i + 1]) for i in range(0, len(arguments) - 1, 2)]
    if len(arguments) % 2 != 0:
        last_string = arguments[-1]
    else:
        last_string = None

    response = ""
    for pair in pairs:
        response = response + (f"``{pair[0]}`` pairs with ``{pair[1]}``\n")
    if last_string:
        response = response + (f"``{last_string}`` is lonely lol")

    # Send message
    destination_channel = client.get_channel(channel_id)
    if destination_channel is None:
        await log(f"[PAIRS] Failed to get destination channel with ID {channel_id}")
        return
    await log(f"[PAIRS] Sending -> {response}")
    await destination_channel.send(f"{response}")
