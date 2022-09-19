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
            if str(message.author) in db["banned"]:
                try:
                    await message.channel.send("Kvůli tvým nevhodným přiznáním ti byla odebrána možnost psát další")
                except discord.errors.Forbidden:
                    pass
            else:
                try:
                    await message.channel.send("Díky za přiznání, za chvíli ho zveřejním")
                    await bot.get_channel(1014200735212249088).send(message.content)  #odeslání textu zprávy do správného kanálu
                except discord.errors.Forbidden:
                    pass
                id = 0
                for key in db.keys():
                    if key != "banned":
                        if int(key) > id:
                            id = int(key)
                while 1:
                    id +=1
                    if str(id) not in db.keys():
                        db[str(id)] = [str(message.content), str(message.author), datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Published"]
                        break
    await bot.process_commands(message)  #zkontroluje jestli zpráva není command

@bot.command(name="year_up", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def role_change(ctx):
    check = await ctx.send("Are you sure you want to move all students to next year?")
    await check.add_reaction("✅")
    def check(reaction, user):
        return user == ctx.author
    try: 
        reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
        if str(reaction.emoji) == "✅":
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
                await ctx.send("Names of roles and channels changed to match current school year")
    except: 
        await ctx.send("Cancelled")

@bot.command(name="list", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def db_list(ctx):
    message = "Total messages - {0}\n".format(len(db.keys())-1)
    for key in db.keys():
        if key == "banned":
            message += ("{0} - {1}\n".format(key, list(db[key])))
            message += ("------------------------------------\n")
    highest_id = 0
    for key in db.keys():
        if key != "banned":
            if int(key) > highest_id:
                highest_id = int(key)
    for id in range(highest_id+1): 
        for key in db.keys():
            if key == str(id):
                message += ("{0} - {1}\n".format(key, list(db[key])))
    await ctx.send(message)

@bot.command(name="del", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def db_delete(ctx, id):
    if str(id) in db.keys():
        check = await ctx.send("Are you sure you want to delete this message?")
        await check.add_reaction("✅")
        def check(reaction, user):
            return user == ctx.author
        try: 
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            if str(reaction.emoji) == "✅":
                try:
                    del db[id]
                except:
                    await ctx.send("Message couldn't be deleted")
                else:
                    await ctx.send("Message deleted from database")
        except: 
            await ctx.send("Cancelled")
    else:
        await ctx.send("No message with that id in database")

load_dotenv()  #načtení tokenu z .env
bot.run(os.getenv('TOKEN'))