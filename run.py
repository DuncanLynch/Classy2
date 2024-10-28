import discord
from discord.ext import commands
import asyncio
import time

bot = discord.Bot()

tokenfile = open("token.txt", "r")
token = str(tokenfile.read())   
#294205336640

@bot.command(description="Send's the bot's latency.")
async def ping(ctx):
    await ctx.respond(bot.latency)

bot.run(token)