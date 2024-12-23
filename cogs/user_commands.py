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
    wishlist = {}

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
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
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
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
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
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
                for i in classdata[:24]:
                    embed.add_field(name=i[2], value = "", inline=False)
                await ctx.followup.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description="", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
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
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
                for i in classdata[:24]:
                    embed.add_field(name=i[2], value = "", inline=False)
                await ctx.followup.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description=f"", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
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
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
                for i in classdata[:24]:
                    embed.add_field(name=i[2], value = "", inline=False)
                await ctx.followup.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description="", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
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
                    embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
                    for i in classdata[:24]:
                        embed.add_field(name=i[2], value = "", inline=False)
                    await ctx.followup.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(title="No courses found with the keyword: '" + keyword +"' in column '" + ln +"'",description="", color=discord.Color.brand_red())
                    embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                    embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
                    await ctx.followup.send(embed=embed)
                    return
    @classes.command(name="help")
    async def help(self,ctx):
        embed = discord.Embed(title = "Help", description="All of the commands that Classy2 has to offer:", color = discord.Color.brand_green())
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
        embed.add_field(name="Query", value="Queries a database of all of the classes in the Stevens Academic Catalogue.")
        embed.add_field(name="Search",value="Searches a certain section of the database for particular keywords.")
        embed.add_field(name="Sync",value="A command only available to the owner of the app, syncs the global commands after restarts to speed up the process.")
        embed.add_field(name="Info",value="Displays all of the creator's (me) info.")
        embed.add_field(name="Wishlist View",value="Provies a user all of the items from their wishlist. WARNING: Currently all wishlist items are not saved to a database, so if the bot goes down, the wishlist will be emptied.")
        embed.add_field(name="Wishlist Add", value="Adds a particular class to the user's wishlist")
        embed.add_field(name="Wishlist Remove", value="Removes a particular item from the user's wishlist if it is present.")
        embed.add_field(name="Wishlist Clear", value="Clears all classes from a user's wishlist.")
        await ctx.respond(embed=embed)
    @classes.command(name="info",description="Displays all of the creator's (me) info.")
    async def info(self,ctx):
        embed = discord.Embed(title = "Shameless Plug", description="Hello! My name is Duncan/Hypa and I recreated and updated our beloved Classy! I'm a 2/3 CS Major set to graduate in the Spring of 2026! ^-^", color = discord.Color.greyple())
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
        embed.add_field(name="GitHub", value="github.com/DuncanLynch", inline=True)
        embed.add_field(name="Linkedin",value="Linkedin.com/in/DuncanLynch", inline=True)
        embed.add_field(name="Contact",value="If for any reason you need to contact me, feel free to shoot me a DM!")
        await ctx.respond(embed=embed)
    wishlistS = classes.create_subgroup("wishlist", "Has wishlist items.")
    @wishlistS.command(name="view",description="Provies a user all of the items from their wishlist.")
    async def view(self,ctx):
        await ctx.defer()
        if self.wishlist.get(ctx.author.name):
            embed = discord.Embed(title = ctx.author.name + "'s Wishlist", description="", color = discord.Color.brand_green())
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
            for i in self.wishlist[ctx.author.name][:25]:
                embed.add_field(name = i[0] +" " + i[1], value = i[2])
            await ctx.followup.send(embed=embed)
        else:
            embed = discord.Embed(title = "Error!", description=f"Error fetching {ctx.author.name}'s wishlist! No items found.", color = discord.Color.brand_red())
            await ctx.followup.send(embed=embed)
    @wishlistS.command(name = "add", description="Adds a particular class to the user's wishlist")
    async def add(self,ctx,school,code):
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
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
            await ctx.followup.send(embed=embed)
            return
            #no class found method
        if self.wishlist.get(ctx.author.name):
            if len(self.wishlist[ctx.author.name]) == 25:
                embed = discord.Embed(title="Wishlist Full!",description=f"Wishlist is currently full and cannot add {school.upper()} {code}. Please remove an item or clear the wishlist!", color=discord.Color.brand_red())
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
                await ctx.followup.send(embed=embed)
                return
        for i in classdata:
            #create and send embed object per class
            connection = sqlite3.connect("classdata.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO analytics (username,classtype,classcode,hitormiss) VALUES (?,?,?,?)", (str(ctx.user.name), school.upper(), code, "hit"))
            connection.commit()
            connection.close()
            if self.wishlist.get(ctx.author.name):
                self.wishlist[ctx.author.name] = self.wishlist[ctx.author.name] + [[i[0],i[1],i[2]]]
            else:
                self.wishlist[ctx.author.name] = [[i[0],i[1],i[2]]]
        embed = discord.Embed(title=(school.upper() + " " + code),description=f"{school.upper()} {code} has been successfully added to the wishlist.", color=discord.Color.brand_green())
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
        await ctx.followup.send(embed=embed)
    @wishlistS.command(name = "remove", description="Removes a particular item from the user's wishlist if it is present.")
    async def remove(self,ctx,school: str,code: str):
        await ctx.defer()
        if self.wishlist.get(ctx.author.name):
            embed = discord.Embed(title = "Success!", description="If the class was in " +ctx.author.name + "'s Wishlist, it was removed.", color = discord.Color.brand_green())
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
            l = []
            for i in self.wishlist[ctx.author.name]:
                if i[0] == school.upper() and i[1] == code:
                    continue
                else:
                    l += [i]
            self.wishlist[ctx.author.name] = l
            await ctx.followup.send(embed=embed)
        else:
            embed = discord.Embed(title = "Error!", description=f"Error fetching {ctx.author.name}'s wishlist! No items found.", color = discord.Color.brand_red())
            await ctx.followup.send(embed=embed)
    @wishlistS.command(name="clear",description="Clears all classes from a user's wishlist.")
    async def clear(self,ctx):
        await ctx.defer()
        if self.wishlist.get(ctx.author.name):
            embed = discord.Embed(title = "Success!", description=ctx.author.name + "'s Wishlist was cleared.", color = discord.Color.brand_green())
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_author(name = "Classy2", icon_url=self.bot.user.avatar)
            self.wishlist[ctx.author.name] = []
            await ctx.followup.send(embed=embed)
        else:
            embed = discord.Embed(title = "Error!", description=f"Error fetching {ctx.author.name}'s wishlist! No items found.", color = discord.Color.brand_red())
            await ctx.followup.send(embed=embed)
def setup(bot):
    bot.add_cog(classes(bot))