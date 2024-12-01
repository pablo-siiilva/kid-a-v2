import asyncio
import random

from printutil import log

from googleapiclient.discovery import build
from datetime import datetime, timedelta

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
        "Would you cry to this song?"
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
        video_id, video_title, video_url = True, "Michael Jackson - Thriller", "https://www.youtube.com/watch?v=sOnqjkJTMaA"
        prompt = "🎃 Spooky OOOOOHHH!!!! Happy Halloween! :D 👻"
    elif now.month == 7 and now.day == 4:
        video_id, video_title, video_url = True, "America, Fuck Yeah! Ultimate Edition", "https://www.youtube.com/watch?v=7R5A0pg4oN8"
        prompt = "So... America!?"
    elif now.month == 4 and now.day == 1:
        video_id, video_title, video_url = True, "Rick Astley - Never Gonna Give You Up", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        prompt = "Lol"
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
        await log(f"[SONG OF THE DAY] Sending: ${message}")

        sent_message = await channel.send(message)

        await sent_message.add_reaction("🥵")
        await sent_message.add_reaction("😐")
        await sent_message.add_reaction("🥶")
        await sent_message.create_thread(f"${now.day}/${now.month}/${now.year} - ${video_title}")


async def initialize(client, youtube_api_token):
    await log("[SONG OF THE DAY] INITIALIZING RANDOM SONG MODULE")
    youtube = build('youtube', 'v3', developerKey=youtube_api_token)
    await log("[SONG OF THE DAY] RANDOM SONG MODULE INITIALIZED SUCCESSFULLY")

    while True:
        now = datetime.now()
        next_run = datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=12)
        if now >= next_run:
            next_run += timedelta(days=1)
        sleep_duration = (next_run - now).total_seconds()
        await log(f"[SONG OF THE DAY] Sleeping for {sleep_duration} seconds until next random song at {next_run}")
        await asyncio.sleep(sleep_duration)
        await send_video(client, youtube)
