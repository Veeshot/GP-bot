import discord
from discord.ext import commands
from datetime import date, datetime
from replit import db

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

def setup(bot): # Must have a setup function
    bot.add_cog(Commands(bot)) # Add the class to the cog.