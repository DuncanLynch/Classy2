import discord
from discord.ext import commands
import asyncio
import time

bot = discord.Bot()

tokenfile = open("token.txt", "r")
token = str(tokenfile.read())   
start = time.time()

@bot.slash_command(name = "sync")
async def sync(ctx):
    await ctx.defer()
    if (ctx.author.name != "hypadeficit"):
        await ctx.followup.send("You are not authorized to run this command...")
        return
    curtime = time.time()
    await bot.sync_commands()
    await ctx.followup.send(f"The commands have synced after {(time.time()-curtime):.2f} seconds.")
    return

@bot.event
async def on_ready():
    newtime = time.time()-start
    print(f"Bot is ready after {newtime:.2f} seconds.")
    await bot.sync_commands()
    print(f"Commands have synced after {(time.time()-start):.2f} seconds.")

bot.load_extension('cogs.user_commands')
bot.run(token)
