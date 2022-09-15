import discord, os
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
from replit import db

intents = discord.Intents.default()  #oprávnění bota
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(intents=intents, command_prefix='?')

cog_files = ["commands"]

for cog_file in cog_files:
    bot.load_extension(cog_file)
    print("{} has benn loaded.".format(cog_file))

@bot.event
async def on_ready():  #co se má stát v moment co je bot připojen a připraven
    print('{0.user} is now online'.format(bot))

@bot.event
async def on_message(message):  #co se má stát, že někdo odešle zprávu
    if message.author != bot.user:  #zajišťuje, že bot nereaguje na své zprávy
        if not message.guild:  #omezuje přijaté zprávy, na které bot bude reagovat, pouze na zprávy v jeho DMs
            try:
                await message.channel.send(
                    "Díky za přiznání, za chvíli ho zveřejním")
                await bot.get_channel(1014200735212249088).send(message.content)  #odeslání textu zprávy do správného kanálu
            except discord.errors.Forbidden:
                pass
            id = str(len(db.keys()-1))
            while 1:
                if str(id) in db.keys():
                    id = int(id)
                    id +=1
                else:
                    db[str(id)] = [str(message.content), str(message.author), datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Published"]
                    break
    await bot.process_commands(message)  #zkontroluje jestli zpráva není command

load_dotenv()  #načtení tokenu z .env
bot.run(os.getenv('TOKEN'))