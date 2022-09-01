import discord, os
from discord.ext import tasks
from dotenv import load_dotenv
from replit import db

if "přiznání" not in db.keys():
    db["přiznání"] = []

intents = discord.Intents.default() #oprávnění bota
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event 
async def on_ready(): #co se má stát v moment co je bot připojen a připraven
    publish.start() #spustí loop s funkcí publish
    print('{0.user} is now online'.format(client))
    print('There are currently {0} messages pending to be published'.format(len(db["přiznání"])))
    
@client.event
async def on_message(message): #co se má stát, že někdo odešle zprávu
    if message.author != client.user: #zajišťuje, že bot nereaguje na své zprávy
        if not message.guild: #omezuje přijaté zprávy, na které bot bude reagovat, pouze na zprávy v jeho DMs
            try:
                await message.channel.send("Díky za přiznání, za chvíli ho zveřejním")
            except discord.errors.Forbidden:
                pass
            db["přiznání"].append(message.content)
          
@tasks.loop(minutes = 10) #kód v bloku by se měl opakovat každých 10 sekund
async def publish():
    if len(db["přiznání"]) != 0:
        channel = client.get_channel(971114306601107536) #objekt channel, s id kanálu #test-room - později se změní na #přiznání
        await channel.send(db["přiznání"][0]) #odeslání textu zprávy do správného kanálu
        db["přiznání"].pop(0)

load_dotenv() #načtení tokenu z .env
client.run(os.getenv('TOKEN'))