import discord
import logging
from discord.ext import commands
import json
import datetime
from datetime import timedelta, datetime
import cogs
from core.PDF_Functions import *
from cogs.mainPDF import *

class SkeletonCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id and payload.guild_id == None and payload.user_id in AuthUsers:
            user = await self.bot.fetch_user(payload.user_id)
            channelFetch = await self.bot.fetch_channel(payload.channel_id)
            message = await channelFetch.fetch_message(payload.message_id)
            timestamp = datetime.now()
            embed = message.embeds[0]
            footer = embed.footer.text
            randomStuff, ID = footer.split(" | ")

            if payload.user_id == 544724467709116457:
                AdultName = "Ethan Hsu"
            elif payload.user_id == 229244813659209738:
                AdultName = "Jason Mei"
            elif payload.user_id == 392811824082583552:
                AdultName = "Paige Delancey"
            elif payload.user_id == 450476337954553858:
                AdultName = "Max Konzerowsky"
            #elif F_supervisor == "Shane":
                #ID = 690709453074464789
            elif payload.user_id == 644918892849790997:
                AdultName = "Atsi Gupta"
            elif payload.user_id == 409152798609899530:
                AdultName = "Space"
            else:
                await user.send("bro who are you???")
                return
            if str(payload.emoji) == "✅":
                Date = timestamp.strftime("%m/%d/%Y")
                await doBottom(Date, AdultName, payload.user_id, ID, self)

            elif str(payload.emoji) == "❌":
                embed = discord.Embed(title = "Rejected Request", description = "You have rejected this user's request and they will not receive their PDF.", color = 0xf55538)
                await user.send(embed = embed)

                endUser = await self.bot.fetch_user(ID)
                embed = discord.Embed(title = "Rejected Request", description = "Dear User, im afraid your request has been denied from your supervisor. If you believe that this is an error, please contact them.", color = 0xf55538)
                endUser.send(embed = embed)
                
            else:
                return

            await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        #if message.author.id == self.bot.id:
            #return
        return
        if message.channel.id == 813109417267429386:
            embed = message.embeds[0]
            student_name = embed.fields[4].value
            student_id = embed.fields[6].value
            school_name = embed.fields[10].value
            school_phone = embed.fields[11].value
            student_address = embed.fields[7].value
            student_city = embed.fields[8].value
            student_state = embed.fields[9].value
            student_email = embed.fields[5].value
            stuff_done = embed.fields[14].value
            await DMPDF(student_name, student_id,school_name,school_phone,student_address,student_city,student_state,student_email, stuff_done,self)


def setup(bot):
    bot.add_cog(SkeletonCMD(bot))