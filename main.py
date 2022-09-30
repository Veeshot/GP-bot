import discord, os, asyncio
from discord.ext import commands
from datetime import date, datetime, timedelta
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
            reply=""
            allowed=True
            print(len(str(message.content)))
            if str(message.author) in db["banned"]:
                reply="Kvůli tvým nevhodným přiznáním ti byla odebrána možnost psát další"
                allowed=False
            elif len(str(message.content)) > 1800:
                reply="Tvoje, přiznání je příliš dlouhé, prosím zkrať ho a pošli znovu"
                allowed=False
            else:
                for key in db.keys(): #spam limiter
                    if key != "banned" and list(db[key])[1]==str(message.author): 
                        delta = datetime.now() - datetime.strptime(list(db[key])[2], "%d/%m/%Y %H:%M:%S")
                        if delta < timedelta(minutes=10):
                            remaining=str(timedelta(minutes=10)-delta)
                            reply="Než budeš moct poslat další přiznání musíš počkat ještě chvilku počkat. Zbývající čas: {0}".format(remaining[3:7])
                            allowed=False
            if allowed:
                id = 0
                for key in db.keys(): #highest id in DB
                    if key != "banned":
                        if int(key) > id:
                            id = int(key)
                while 1: #save to DB
                    id +=1
                    if str(id) not in db.keys():
                        db[str(id)] = [str(message.content), str(message.author), datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Published"]
                        break
                while str(id) not in db.keys():
                    await asyncio.sleep(1)
                try:
                    reply="Díky za přiznání, hned ho zveřejním"
                    await bot.get_channel(1014200735212249088).send(message.content) #odeslání textu zprávy do správného kanálu
                except discord.errors.Forbidden:
                    pass
            await message.channel.send(reply)
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
            for id in range(8):
                list_8=["V8","V7","V6","V5","V4","V3","V2","V1"]
                if id==0:
                    await discord.utils.get(ctx.guild.roles,name="V8").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 8)[-2:],str(date.today().year)[-2:]))
                    await discord.utils.get(ctx.guild.categories,name="V8").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 8)[-2:],str(date.today().year)[-2:]))
                else:
                    await discord.utils.get(ctx.guild.roles, name=list_8[id]).edit(name=list_8[id-1])
                    await discord.utils.get(ctx.guild.categories, name=list_8[id]).edit(name=list_8[id-1])
            for id in range(4):
                list_4=["4.A","3.A","2.A","1.A"]
                if id==0:
                    await discord.utils.get(ctx.guild.roles,name="4.A").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 4)[-2:],str(date.today().year)[-2:]))
                    await discord.utils.get(ctx.guild.categories,name="4.A").edit(name="Absolvent {0}-{1}".format(str(date.today().year - 4)[-2:],str(date.today().year)[-2:]))
                else:
                    await discord.utils.get(ctx.guild.roles, name=list_4[id]).edit(name=list_4[id-1])
                    await discord.utils.get(ctx.guild.categories, name=list_4[id]).edit(name=list_4[id-1])
            for id in range(2):
                list_2=["V1","1.A"]
                await ctx.guild.create_role(name=list_2[id])
                await ctx.guild.create_category(name=list_2[id]) 
                await discord.utils.get(ctx.guild.categories, name=list_2[id]).set_permissions(ctx.guild.default_role, view_channel=False)
                await discord.utils.get(ctx.guild.categories, name=list_2[id]).set_permissions(discord.utils.get(ctx.guild.roles, name=list_2[id]), view_channel=True, connect=True)
                await discord.utils.get(ctx.guild.categories, name=list_2[id]).set_permissions(discord.utils.get(ctx.guild.roles, name="Třídní admin"), manage_channels=True, manage_permissions=True, manage_webhooks=True, create_instant_invite=True, send_messages=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True, embed_links=True, attach_files=True, add_reactions=True, use_external_emojis=True, use_external_stickers=True, mention_everyone=True, manage_messages=True, manage_threads=True, read_message_history=True, send_tts_messages=True, use_application_commands=True, connect=True, speak=True, stream=True, use_voice_activation=True, mute_members=True, deafen_members=True, move_members=True, manage_events=True,)
                await discord.utils.get(ctx.guild.categories, name=list_2[id]).set_permissions(discord.utils.get(ctx.guild.roles, name="ADMIN-BOTI"), view_channel=True, connect=True)
                await ctx.guild.create_text_channel(name = "třídní-chat", category=discord.utils.get(ctx.guild.categories, name=list_2[id]))
                await ctx.guild.create_voice_channel(name = "Třídní voice", category=discord.utils.get(ctx.guild.categories, name=list_2[id]))
                await discord.utils.get(ctx.guild.channels,name="třídní-chat").edit(sync_permissions=True)
                await discord.utils.get(ctx.guild.channels,name="Třídní voice").edit(sync_permissions=True)
            await ctx.send("Names of roles and channels changed to match current school year")
    except asyncio.TimeoutError: 
        await ctx.send("Timed out")

@bot.command(name="list", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def db_list(ctx):
    message = "Total messages - {0}\n".format(len(db.keys())-1)
    for key in db.keys():
        if key == "banned":
            message += ("{0} - {1}\n".format(key, list(db[key])))
            message += ("------------------------------------\n")
    highest_id = 0
    for key in db.keys(): #highest ID -> for how many times cycle shoud repeat
        if key != "banned":
            if int(key) > highest_id:
                highest_id = int(key)
    try:
        for id in range(highest_id+1):
            for key in db.keys():
                if key == str(id):
                    new = "{0} - {1}\n".format(key, list(db[key]))
                    if (len(message) + len(new)) >= 2000:
                        await ctx.send(message)
                        message=""
                    message += new
        if len(message) !=0:
            await ctx.send(message)
    except Exception as e:
       await ctx.send("Failed due to {}".format(e))

@bot.command(name="listfile", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def file_list(ctx):
    highest_id = 0
    for key in db.keys(): #highest ID -> for how many times cycle shoud repeat
        if key != "banned":
            if int(key) > highest_id:
                highest_id = int(key)
    try:
        file = open("db.txt", "w")
    except Exception as e:
       await ctx.send("Failed due to {}".format(e))
    else:
        file.write("Total messages - {0}\n".format(len(db.keys())-1))
        for key in db.keys():
            if key == "banned":
                file.write("{0} - {1}\n".format(key, list(db[key])))
                file.write("------------------------------------\n")
        for id in range(highest_id+1):
            for key in db.keys():
                if key == str(id):
                    file.write("{0} - {1}\n".format(key, list(db[key])))
    await asyncio.sleep(5)
    await ctx.send(file=discord.File("db.txt")) #sending blank file
    #os.remove("db.txt")
    
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
        
@bot.command(name="delall", pass_context=True)
@commands.has_any_role("Full admin", "Full admin vol.2")  #příkaz mohou používat pouze určité role
async def db_erase(ctx):
    check = await ctx.send("Are you sure you want to erase **whole** DB?")
    await check.add_reaction("✅")
    def check(reaction, user):
        return user == ctx.author
    try: 
        reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
        if str(reaction.emoji) == "✅":
            try:
                for key in db.keys():
                    if key != "banned":   
                        del db[key]
            except:
                await ctx.send("DB could not be erased")
            else:
                await ctx.send("All entries from DB erased")
    except: 
        await ctx.send("Cancelled")

load_dotenv()  #načtení tokenu z .env
bot.run(os.getenv('TOKEN'))