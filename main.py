import discord, os
from discord.ext import commands
from datetime import date, datetime
from dotenv import load_dotenv
from replit import db

intents = discord.Intents.default()  #oprávnění bota
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(intents=intents, command_prefix='?')

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
            db[str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))] = (str(message.author), str(message.content))
    await bot.process_commands(message)  #zkontroluje jestli zpráva není command

@bot.command(name="year_up", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def role_change(ctx):
    await discord.utils.get(ctx.guild.roles,name="V8").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 8)[-2:],str(date.today().year)[-2:]))
    await discord.utils.get(ctx.guild.roles,name="4.A").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 4)[-2:],str(date.today().year)[-2:]))
    await discord.utils.get(ctx.guild.roles, name="V7").edit(name="V8")
    await discord.utils.get(ctx.guild.roles, name="3.A").edit(name="4.A")
    await discord.utils.get(ctx.guild.roles, name="V6").edit(name="V7")
    await discord.utils.get(ctx.guild.roles, name="2.A").edit(name="3.A")
    await discord.utils.get(ctx.guild.roles, name="V5").edit(name="V6")
    await discord.utils.get(ctx.guild.roles, name="1.A").edit(name="2.A")
    await discord.utils.get(ctx.guild.roles, name="V4").edit(name="V5")
    await discord.utils.get(ctx.guild.roles, name="V3").edit(name="V4")
    await discord.utils.get(ctx.guild.roles, name="V2").edit(name="V3")
    await discord.utils.get(ctx.guild.roles, name="V1").edit(name="V2")
    await ctx.guild.create_role(name="V1")
    await ctx.guild.create_role(name="1.A")
    await discord.utils.get(ctx.guild.categories,name="V8").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 8)[-2:],str(date.today().year)[-2:]))
    await discord.utils.get(ctx.guild.categories,name="4.A").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 4)[-2:],str(date.today().year)[-2:]))
    await discord.utils.get(ctx.guild.categories, name="V7").edit(name="V8")
    await discord.utils.get(ctx.guild.categories, name="3.A").edit(name="4.A")
    await discord.utils.get(ctx.guild.categories, name="V6").edit(name="V7")
    await discord.utils.get(ctx.guild.categories, name="2.A").edit(name="3.A")
    await discord.utils.get(ctx.guild.categories, name="V5").edit(name="V6")
    await discord.utils.get(ctx.guild.categories, name="1.A").edit(name="2.A")
    await discord.utils.get(ctx.guild.categories, name="V4").edit(name="V5")
    await discord.utils.get(ctx.guild.categories, name="V3").edit(name="V4")
    await discord.utils.get(ctx.guild.categories, name="V2").edit(name="V3")
    await discord.utils.get(ctx.guild.categories, name="V1").edit(name="V2")
    print("Names of roles and channels changed to match current school year")

load_dotenv()  #načtení tokenu z .env
bot.run(os.getenv('TOKEN'))