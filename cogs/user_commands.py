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
"EN", "TM"]
coursecodes.sort()
class classes(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("Class commands Cog is initialized.")

    classes = discord.SlashCommandGroup("classy", "A command regarding classes at Steven's Institute of Technology")



    @classes.command(name = "query")
    async def classyquery(self, ctx, school: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(coursecodes)), code):
        await ctx.defer()
        connection = sqlite3.connect("classdata.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM classes WHERE classtype = ? AND classcode = ?", (str(school.upper()), str(code)))        
        classdata = cursor.fetchall()
        cursor.close()
        if not classdata:
            connection = sqlite3.connect("classdata.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO analytics (username,classtype,classcode,hitormiss) VALUES (?,?,?,?)", (str(ctx.user.name), school.upper(), code, "miss"))
            connection.commit()
            connection.close()
            embed = discord.Embed(title=(school.upper() + " " + code),description=f"No class by the name of {school.upper()} {code} has been found in the database.", color=discord.Color.brand_red())
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
            await ctx.followup.send(embed=embed)
            return
            #no class found method
        for i in classdata:
            #create and send embed object per class
            connection = sqlite3.connect("classdata.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO analytics (username,classtype,classcode,hitormiss) VALUES (?,?,?,?)", (str(ctx.user.name), school.upper(), code, "hit"))
            connection.commit()
            connection.close()
            embed = discord.Embed(title = i[2], description = i[3], color = discord.Color.brand_green(), url=i[8])
            embed.add_field(name = "Credits", value=i[7])
            if i[4]:
                embed.add_field(name="Pre-requisites", value =i[4], inline = True)
            if i[5]:
                embed.add_field(name="Co-requisites", value =i[5], inline = True)
            if i[6]:
                embed.add_field(name="Typically offered periods", value =i[6])
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
            await ctx.followup.send(embed=embed)
        return
    
    @classes.command(name="search")
    async def search(self,ctx,keyword: str, ln: discord.Option(str, choices=["Course Title", "Course Description", "Prerequisites", "Corequisites"])):
        await ctx.defer()
        kw = "%" + keyword + "%"
        if ln == "Course Title":   
            connection = sqlite3.connect("classdata.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM classes WHERE classtitle LIKE ?", (kw,))        
            classdata = cursor.fetchall()
            cursor.close()
            if classdata:
                embed = discord.Embed(title = "Search in the database for: '" + keyword +"' in column " + ln +"'", description="", color = discord.Color.brand_green())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                for i in classdata[:24]:
                    embed.add_field(name=i[2], value = "", inline=False)
                await ctx.followup.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description="", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                await ctx.followup.send(embed=embed)
                return
        if ln == "Course Description":   
            connection = sqlite3.connect("classdata.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM classes WHERE classdescription LIKE ?", (kw,))        
            classdata = cursor.fetchall()
            cursor.close()
            if classdata:
                embed = discord.Embed(title = "Search in the database for: '" + keyword +"' in column " + ln +"'", description="", color = discord.Color.brand_green())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                for i in classdata[:24]:
                    embed.add_field(name=i[2], value = "", inline=False)
                await ctx.followup.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description=f"", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                await ctx.followup.send(embed=embed)
                return
        if ln == "Prerequisites":   
            connection = sqlite3.connect("classdata.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM classes WHERE prerequisites LIKE ?", (kw,))        
            classdata = cursor.fetchall()
            cursor.close()
            if classdata:
                embed = discord.Embed(title = "Search in the database for: '" + keyword +"' in column " + ln +"'", description="", color = discord.Color.brand_green())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                for i in classdata[:24]:
                    embed.add_field(name=i[2], value = "", inline=False)
                await ctx.followup.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description="", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                await ctx.followup.send(embed=embed)
                return
        if ln == "Corequisites":   
                connection = sqlite3.connect("classdata.db")
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM classes WHERE corequisites LIKE ?", (kw,))        
                classdata = cursor.fetchall()
                cursor.close()
                if classdata:
                    embed = discord.Embed(title = "Search in the database for: '" + keyword +"' in column " + ln +"'", description="", color = discord.Color.brand_green())
                    embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                    embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                    for i in classdata[:24]:
                        embed.add_field(name=i[2], value = "", inline=False)
                    await ctx.followup.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description="", color=discord.Color.brand_red())
                    embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                    embed.set_author(name = "Classy2 by Duncan Lynch", icon_url=self.bot.user.avatar)
                    await ctx.followup.send(embed=embed)
                    return

def setup(bot):
    bot.add_cog(classes(bot))