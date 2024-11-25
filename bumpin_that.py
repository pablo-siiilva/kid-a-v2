import threading
import time

FOUR_HOURS = 14400


async def initialize(client, channel):
    print("INITIALIZING BUMP MODULE")

    async def wrapper():
        while True:
            print("BUMPING THAT")
            await client.get_channel(channel).send("https://cdn.discordapp.com/attachments/637679343740649512/1310461793294094356/Sem_titulo.png?ex=67454e26&is=6743fca6&hm=83f55dfdf8ea755af978556c41f1e5e6d59e7f32af9cbebb3a2b060227ccd529&")
            print("WAITING FOUR MORE HOURS FOR BUMP")
            time.sleep(FOUR_HOURS)

    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()

    print("BUMP MODULE INITIALIZED SUCCESSFULLY")
