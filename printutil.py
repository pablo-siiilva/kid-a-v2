client = None


async def log(value):
    global client
    print(value)
    if client:
        await client.get_channel(1312654527261839460).send(value)


def set_client(c):
    global client
    client = c
