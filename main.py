import discord
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('{0.user} is now online'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('/hello'):
        await message.channel.send('Hello!')
        print("answered")
    elif message.author == client.user:
        return

load_dotenv()
client.run(os.getenv('TOKEN'))