import discord
from dotenv import load_dotenv
import os

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('{0.user} is now online'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        print("answered")

load_dotenv()
client.run(os.getenv('TOKEN'))