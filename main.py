import discord
import time
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID_ORIGINAL = 1246881463266181171  # ID for #one-word-each
CHANNEL_ID_DESTINATION = 1256777917468381246  # ID for the finished sentences channel
CHANNEL_ID_DESTINATION_RANDOM = 1243270048295026811  # ID for general chat

# Configurar intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# Lista para armazenar as palavras
words = []

# Função para formar uma sentença a partir das palavras
def form_sentence():
    return ' '.join(words)

# Função para buscar o histórico de mensagens
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

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    try:
        original_channel = client.get_channel(CHANNEL_ID_ORIGINAL)
        if original_channel is None:
            print(f"Failed to get channel with ID {CHANNEL_ID_ORIGINAL}")
            return
        await fetch_message_history(original_channel)
        print(f"Fetched messages: {words}")
    except Exception as e:
        print(f"Error in on_ready: {e}")

@client.event
async def on_message(message):
    try:
        if message.channel.id == CHANNEL_ID_ORIGINAL and not message.author.bot:
            print(f"New message in #{message.channel.name} by {message.author.name}: {message.content}")
            words.append(message.content)
            if message.content.endswith(('.', '!', '?')):  # Verificar se a sentença está completa
                destination_channel = client.get_channel(CHANNEL_ID_DESTINATION)
                if destination_channel is None:
                    print(f"Failed to get destination channel with ID {CHANNEL_ID_DESTINATION}")
                    return
                sentence = form_sentence()
                print(f"Sending sentence: {sentence}")
                await destination_channel.send(f"#one-word-each has just finished a new sentence.\n"
                                               f"<t:{int(time.time())}>: {sentence}")
                words.clear()
    except Exception as e:
        print(f"Error in on_message: {e}")

print("Starting bot...")
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Error running the bot: {e}")
