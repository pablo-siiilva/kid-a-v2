import asyncio
import random
from datetime import timedelta

from googleapiclient.discovery import build
from datetime import datetime, timedelta


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
        "Today's track is:"
        "What do you think about this track?"
        "What are your thoughts on this song?"
        "Are you a fan of this song?"
        "How are you feeling on this song?"
        "Ever heard this one before?"
        "Here's a listen for ya!"
        "Here's a listen for ya!"
        "Here's a listen for ya!"
        "Here's a listen for ya!"
        "Here's a listen for ya!"
        "Here's a song for you!"
        "Here's a song for you!"
        "Here's a song for you!"
        "Here's a song for you!"
        "Here's a song for you!"
        "Would you cry to this song?"
    ])


async def send_video(bot, youtube):
    print("Time for sending a song!")
    playlist_id = "PLVADazPd2uMGe7D3fkGYCbizIhNZCUqWo"
    print("Finding item on playlist")
    video_id, video_title, video_url = get_random_video_from_playlist(youtube, playlist_id)

    if video_id:
        channel = bot.get_channel(1243270048295026811)
        prompt = pick_random_prompt()
        message = f"🎶 {prompt} 🎶 \n**{video_title}**\n{video_url}"
        print("Sending: " + message)

        sent_message = await channel.send(message)

        await sent_message.add_reaction("🥵")
        await sent_message.add_reaction("😐")
        await sent_message.add_reaction("🥶")


async def initialize(client, youtube_api_token):
    print("INITIALIZING RANDOM SONG MODULE")
    youtube = build('youtube', 'v3', developerKey=youtube_api_token)
    print("RANDOM SONG MODULE INITIALIZED SUCCESSFULLY")

    while True:
        now = datetime.now()
        next_run = datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=12,
                                                                                 minutes=00)
        if next_run < now:
            next_run += timedelta(days=1)

        sleep_duration = (next_run - now).total_seconds()
        print(f"Sleeping for {sleep_duration} seconds until next random song at {next_run}")
        await asyncio.sleep(sleep_duration)

        await send_video(client, youtube)
