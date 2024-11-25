import threading
import time
import asyncio

FOUR_HOURS = 4 * 60 * 60


async def initialize(client, channel):
    print("INITIALIZING BUMP MODULE")

    async def wrapper():
        while True:
            print("BUMPING THAT")
            await client.get_channel(channel).send("https://cdn.discordapp.com/attachments/637679343740649512/1310461793294094356/Sem_titulo.png?ex=67454e26&is=6743fca6&hm=83f55dfdf8ea755af978556c41f1e5e6d59e7f32af9cbebb3a2b060227ccd529&")
            print("WAITING FOUR MORE HOURS FOR BUMP")
            await asyncio.sleep(FOUR_HOURS)

    await asyncio.create_task(wrapper())
    print("BUMP MODULE INITIALIZED SUCCESSFULLY")
