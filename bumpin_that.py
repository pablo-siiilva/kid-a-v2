import threading
import time
import asyncio

FOUR_HOURS = 4 * 60 * 60


async def initialize(client, channel):
    print("INITIALIZING BUMP MODULE")

    async def wrapper():
        while True:
            print("BUMPING THAT")
            await client.get_channel(channel).send("https://cdn.discordapp.com/attachments/...")
            print("WAITING FOUR MORE HOURS FOR BUMP")
            await asyncio.sleep(FOUR_HOURS)

    await asyncio.create_task(wrapper())
    print("BUMP MODULE INITIALIZED SUCCESSFULLY")
