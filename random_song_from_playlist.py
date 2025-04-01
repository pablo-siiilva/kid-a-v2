import asyncio
import random

from printutil import log

from googleapiclient.discovery import build
from datetime import datetime, timedelta, time

PLAYLIST_ID = "PLVADazPd2uMGe7D3fkGYCbizIhNZCUqWo"

CHANNEL_GENERAL = 1243278540846399641


def get_all_videos_from_playlist(youtube, playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    while request:
        response = request.execute()
        videos.extend(response['items'])
        request = youtube.playlistItems().list_next(request, response)

    return videos


def get_random_video_from_playlist(youtube, playlist_id):
    videos = get_all_videos_from_playlist(youtube, playlist_id)

    if not videos:
        return None, None, None

    # Pick a random video from the list
    random_video = random.choice(videos)
    video_id = random_video['snippet']['resourceId']['videoId']
    video_title = random_video['snippet']['title']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return video_id, video_title, video_url


def pick_random_prompt():
    return random.choice([
        "What do you think about this song??",
        "Hey, check out this one:",
        "Beep beep random song time!",
        "Is this song HOT 🔥🔥🔥 or NOT 🥶🧊🧊??",
        "On a scale of 1 to 10 how good is this song?",
        "Is this song a bop?",
        "Ever heard this song before?",
        "Banger time:",
        "If this song was playing on a Walmart, how would you be feeling?",
        "Is this RYMCore?",
        "Hey hey hey time for a song",
        "Is this one hit or miss?",
        "Is this song replayable to death?",
        "What does this song smell like?",
        "I am a bot and i do not have a conscience, but here's a song:",
        "I am a bot and i do not have a conscience, but this one is a 10/10 certified Fantano classic",
        "Is this a 5 star?",
        "Smash or pass on this one?",
        "Song of the day!",
        "The mailman is at the door and he just brought you a song (and a notice for not paying child support)",
        "Song",
        "Would you cry to this song?",
        "Groovy or snoozy??????",
        "Here's a cool song",
        "Here's a song to brighten your day :)",
        "Here's a song to darken your day >:D",
        "Here's a song to fuck shit up to",
        "Is this aux material?",
        "Today's song is:",
        "Today's song is:",
        "Today's song is:",
        "Today's song is:",
        "Today's song is:",
        "Today's track is:",
        "Today's track is:",
        "Today's track is:",
        "Today's track is:",
        "Today's track is:",
        "What do you think about this track?",
        "What are your thoughts on this song?",
        "Are you a fan of this song?",
        "How are you feeling on this song?",
        "Ever heard this one before?",
        "Here's a listen for ya!",
        "Here's a listen for ya!",
        "Here's a listen for ya!",
        "Here's a listen for ya!",
        "Here's a listen for ya!",
        "Here's a song for you!",
        "Here's a song for you!",
        "Here's a song for you!",
        "Here's a song for you!",
        "Here's a song for you!",
        "Would you cry to this song?",
        "What do you think about this song??",
        "Hey, check out this one:",
        "Beep beep random song time!",
        "Is this song HOT 🔥🔥🔥 or NOT �❄️??",
        "On a scale of 1 to 10 how good is this song?",
        "Is this song a bop?",
        "Ever heard this song before?",
        "Banger time:",
        "If this song was playing in Walmart, how would you be feeling?",
        "Scaruffi recommended me this song... Do you approve it?",
        "Is this /mu/core?",
        "Is this /mu/core?",
        "Is this RYMcore?",
        "Is this RYMcore?",
        "Hey hey hey time for a song",
        "Is this one hit or miss?",
        "Would you listen to this song on your deathbed?",
        "What does this song smell like?",
        "I am a bot and I do not have a conscience, but here's a song:",
        "Certified Fantano 10/10 classic review or Fantano NOT GOOD 0/10 YUNOREVIEW miss???",
        "Is this a 5-star song?",
        "Smash or pass on this one?",
        "Song of the day!",
        "Song.",
        "Would you cry to this song?",
        "Groovy or snoozy??????",
        "Here's a cool song",
        "Here's a song to fuck shit up to",
        "Is this aux material?",
        "What do you think about this track?",
        "What are your thoughts on this song?",
        "Are you a fan of this song?",
        "How are you feeling about this song?",
        "Ever heard this one before?",
        "Here's a listen for ya!",
        "Here's a song for you!",
        "Would you cry to this song?",
        "Slap or flop?",
        "If this song was a food, what would it taste like?",
        "Would you bump this at your funeral",
        "Would you bump this at your aunt's funeral",
        "Banana Split",
        "Is this song a vibe or a crime?",
        "If this song was a person, would they threaten you",
        "If this song was a person, would they scare you",
        "If this song was a person, would they be able to beat you up",
        "If this song was a person, would they be able to beat you up",
        "If this song was a person, would they be able to fuck you up",
        "If this song was a person, would you ... smash? :flushed: ",
        "Would you play this song at your wedding?",
        "does this song radiate main character energy",
        "does this song deserve a restraining order?",
        "If this song was a color, what color would it be???",
        "If this song was a worm, what type of worm would it be???",
        "Would you recommend this song to your mom?",
        "in a scale of cringe to based where does this song fit",
        "DO YOU THINK LIL B THE BASED GOD WOULD APPROVE THIS SONG",
        "you show this song to a date. what's their reaction?",
        "How scary is this song?"
    ])


async def send_video(bot, youtube):
    await log("[SONG OF THE DAY] Time for sending a song!")

    now = datetime.now()
    if now.month == 12 and now.day == 25:
        video_id, video_title, video_url = True, "Wham! - Last Christmas", "https://www.youtube.com/watch?v=E8gmARGvPlI"
        prompt = "🎄 Merry christmas! :D 🎄"
    elif now.month == 2 and now.day == 14:
        video_id, video_title, video_url = True, "Mazzy Star - Fade Into You", "https://www.youtube.com/watch?v=ImKY6TZEyrI"
        prompt = "This one is for all you lonely fucks. Happy valentine's day!"
    elif now.month == 10 and now.day == 31:
        video_id, video_title, video_url = True, "Misfits - Halloween", "https://www.youtube.com/watch?v=Ezuk-v9q_80"
        prompt = "🎃 Spooky OOOOOOOOOHHH!!!! Happy Halloween! :D 👻"
    elif now.month == 4 and now.day == 1:
        video_id, video_title, video_url = True, "AJR - Thirsty", "https://www.youtube.com/watch?v=s3deZAT-XY0"
        prompt = ("AJR is an American pop band founded by brothers Adam, Jack, and Ryan Met (né Metzger), collectively "
                  "a trio of vocalists, multi-instrumentalists, and songwriters.[1] The brothers grew up in New York "
                  "City, primarily focused on busking and singing covers until shifting to songwriting and touring. "
                  "At their home studio, they have recorded more than 100 songs and have released five studio albums "
                  "on various record labels along with their indie label.[a] AJR wrote 'I'm Ready' and promoted the "
                  "song onto Twitter in 2012, which led to Australian singer and songwriter Sia sharing her talent "
                  "management network with the trio prior to the release. After the song became their breakout single "
                  "on radio, AJR formed their own label AJR Productions[7] and released three EPs—6foot1 (2013), "
                  "Infinity (2014), and What Everyone's Thinking (2016). Since their debut, AJR has written or "
                  "co-written every song in their five-album discography: Living Room (2015); The Click (2017); the "
                  "two U.S. Billboard 200 top-ten albums—Neotheater (2019), OK Orchestra (2021); and The Maybe Man ("
                  "2023). The 2017 electropop platinum album contained their first Billboard Alternative number-one "
                  "song 'Sober Up' (featuring Rivers Cuomo), and the 2021 orchestral pop gold album spawned—their "
                  "first Hot 100 top-ten single and the Billboard Music Award Top Rock Song—'Bang!'. AJR is a "
                  "multi-platinum band for having seven platinum singles—including the three aforementioned songs; "
                  "'Weak', 'Burn the House Down', '100 Bad Days', and 'Way Less Sad'—all of which accounted for "
                  "eleven million certified units of their digital single sales in America.[8][9]")
    elif now.month == 4 and now.day == 20:
        video_id, video_title, video_url = True, "Sublime - Smoke Two Joints", "https://www.youtube.com/watch?v=KQnzeKKg7Yc"
        prompt = "Peace and love ☮🌿😻"
    elif now.month == 9 and now.day == 21:
        video_id, video_title, video_url = True, "Earth, Wind & Fire - September", "https://www.youtube.com/watch?v=Gs069dndIYk"
        prompt = "🍂 What day is it again? I don't remember. Do you remember? 🍁"
    else:
        await log("[SONG OF THE DAY] Finding item on playlist...")
        video_id, video_title, video_url = get_random_video_from_playlist(youtube, PLAYLIST_ID)
        prompt = pick_random_prompt()

    if video_id:
        channel = bot.get_channel(CHANNEL_GENERAL)
        message = f"🎶 {prompt} 🎶 \n**{video_title}**\n{video_url}"
        await log(f"[SONG OF THE DAY] Sending: {message}")

        sent_message = await channel.send(message)

        await sent_message.add_reaction("🔥")
        await sent_message.add_reaction("🤷")
        await sent_message.add_reaction("💩")


is_initialized = False


async def initialize(client, youtube_api_token):
    global is_initialized
    if is_initialized:
        await log("[SONG OF THE DAY] Module already initialized. Skipping.")
        return
    is_initialized = True

    await log("[SONG OF THE DAY] INITIALIZING RANDOM SONG MODULE")
    youtube = build('youtube', 'v3', developerKey=youtube_api_token)
    await log("[SONG OF THE DAY] RANDOM SONG MODULE INITIALIZED SUCCESSFULLY")

    while True:
        now = datetime.now()
        next_run = datetime.combine(now.date(), time(hour=12))
        if now >= next_run:
            next_run += timedelta(days=1)
        sleep_duration = (next_run - now).total_seconds()
        await log(f"[SONG OF THE DAY] Sleeping for {sleep_duration} seconds until next random song at {next_run}")
        await asyncio.sleep(sleep_duration)
        await send_video(client, youtube)
