import discord
from discord.ext import commands
import asyncio
import time
import sqlite3
coursecodes = ["HASS",
"HPL",
"HLI",
"MA",
"CS",
"PEP",
"BIO",
"CH",
"ME",
"CE",
"CPE",
"EE",
"ENGR",
"PRV",
"MGT",
"EM",
"BT",
"IDE",
"NANO",
"QF",
"FE",
"ISE",
"SSW",
"SYS",
"OE",
"BME",
"CHE",
"EN"]
coursecodes.sort()
class classes(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Class commands Cog is initialized.")

    classes = discord.SlashCommandGroup("classy", "A command regarding classes at Steven's Institute of Technology")



    @classes.command(name = "query")
    async def classyquery(self, ctx, school, code):
        await ctx.defer()
        connection = sqlite3.connect("classdata.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM classes WHERE classtype = ? AND classcode = ?", (str(school), str(code)))        
        classdata = cursor.fetchall()
        cursor.close()
        if not classdata:
            await ctx.followup.send(f"No class by the name of {school} {code} was found in the database.")
            return
            #no class found method
        for i in classdata:
            #create and send embed object per class
            embed = discord.Embed(title = i[2], description = i[3], color = discord.Color.brand_green())
            embed.add_field(name = "Credits", value=i[7])
            if i[4]:
                embed.add_field(name="Pre-requisites", value =i[4], inline = True)
            if i[5]:
                embed.add_field(name="Co-requisites", value =i[5], inline = True)
            if i[6]:
                embed.add_field(name="Typically offered periods", value =i[6])
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
            await ctx.followup.send(embed=embed)
        return
    

def setup(bot):
    bot.add_cog(classes(bot))