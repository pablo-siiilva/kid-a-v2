import threading
import time
import asyncio

from printutil import log

TWELVE_HOURS = 12 * 60 * 60


async def initialize(client, channel):
    await log("[BUMP] INITIALIZING BUMP MODULE")

    async def wrapper():
        while True:
            await log("[BUMP] WAITING 24 HOURS FOR NEXT BUMP")
            await asyncio.sleep(TWELVE_HOURS)
            await asyncio.sleep(TWELVE_HOURS)
            await log("[BUMP] BUMPING THAT")
            await log("[BUMP] SENDING https://cdn.discordapp.com/attachments/637679343740649512/1310461793294094356/Sem_titulo.png?ex=67454e26&is=6743fca6&hm=83f55dfdf8ea755af978556c41f1e5e6d59e7f32af9cbebb3a2b060227ccd529&")
            await client.get_channel(channel).send("https://cdn.discordapp.com/attachments/637679343740649512/1310461793294094356/Sem_titulo.png?ex=67454e26&is=6743fca6&hm=83f55dfdf8ea755af978556c41f1e5e6d59e7f32af9cbebb3a2b060227ccd529&")

    asyncio.create_task(wrapper())
    await log("[BUMP] BUMP MODULE INITIALIZED SUCCESSFULLY")
