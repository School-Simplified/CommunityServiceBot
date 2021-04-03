from oauth2client.service_account import ServiceAccountCredentials
import gspread
import discord
from discord.ext import commands
from datetime import datetime
import time
import re
import asyncio
from discord import Embed
import logging
import random
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from shutil import copyfile
from core import common
from core.common import load_config
from core.common import prompt_config
import re
import textwrap
from PIL import Image
from PIL import ImageDraw, ImageFont
from core.PDF_Functions import *

config, _ = load_config()


logger = logging.getLogger(__name__)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("School Simplified Inc. Volunteer Hours Form (Responses)").sheet1

add_opt = [
            {
                "name": "org_name",
                "description": "Name of the Organization.",
                "type": 3,
                "required": True
            },
            {
                "name": "org_city",
                "description": "City of the Organization.",
                "type": 3,
                "required": True
            },
            {
                "name": "org_state",
                "description": "State of the Organization.",
                "type": 3,
                "required": True
            },
            {
                "name": "org_phone",
                "description": "Phone Number of the Organization.",
                "type": 3,
                "required": True
            },
            {
                "name": "org_email",
                "description": "Email of the Organization.",
                "type": 3,
                "required": True
            },
            {
                "name": "org_contact_name",
                "description": "Contact Name for the Organization.",
                "type": 3,
                "required": True
            }
        ]

PDF_opt = [
            {
                "name": "query",
                "description": "Query to search for.",
                "type": 3,
                "required": True
            }
        ]


AuthUsers = [544724467709116457, 229244813659209738, 392811824082583552, 450476337954553858, 644918892849790997, 409152798609899530]

class CogCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("PDF: Cog Loaded!")


    @commands.command()
    async def doPDF(self, ctx):
        await ctx.send("m")
        await doBottom("date", "adul", ctx)


    @commands.command()
    async def form(self, ctx):
        await ctx.send("Please check your DMs!")
        channel = await ctx.author.create_dm()
        embed = discord.Embed(title = "READ CAREFULLY!", description = "You are about to fill out a **COMMUNITY SERVICE HOURS FORM**, please make sure you actually answer the question in the best, detailed way possible! A PDF will be generated based on your **exact** responses so triple-check responses before you submit!\n**If you did make a mistake, you will be able to cancel the form and start over!**", color = 0xeb8334)
        embed.set_footer(text = "Starting questions now...")

        await channel.send(embed = embed)

        def check(m):
            return m.content is not None and m.channel == channel and m.author is not self.bot.user

        embed = discord.Embed(title = "Q1-What is your full name?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_fullname = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q2-What is your email address?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_email = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q3-What is your student ID number?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_studentID = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q4-What is your home's street address?" , description =  "**Example:**\n15 Maple St.", color = 0x34eb71)
        await channel.send(embed = embed)
        F_address = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q5-In what city or town do you live in?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_townANDcity = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q6-In what state do you live in?",description = "**DO NOT USE ABBREVIATIONS!**", color = 0x34eb71)
        await channel.send(embed = embed)
        F_state = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q7-What is the name of your school?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_schoolName = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q8-What is the telephone number of your school?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_schoolNumber = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q9-How many hours are you requesting?", description = "If it is above 150 please fill out a separate form!", color = 0x34eb71)
        await channel.send(embed = embed)
        F_numHours = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q10-How did you acquire your service hours?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_hourAcquire = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q11-Who is your supervisor?", description = "**Choices:**\n\n1: **Ethan Hsu**\n2: **Jason Mei**\n3: **Paige Delancey**\n4: **Max Konzerowsky**\n5: **Jade**\n\n**PICK THE CORRESPONDING NUMBER!**\n*Example: Respond with **4** if your supervisor is Max!*", color = 0x34eb71)
        await channel.send(embed = embed)
        F_supervisor = await self.bot.wait_for('message', check=check)

        sV = F_supervisor.content
        print(sV)
        print(type(sV))
        if sV == "1":
            F_supervisor2 = "Ethan Hsu"
        elif sV == "2":
            F_supervisor2 = "Jason Mei"
        elif sV == "3":
            F_supervisor2 = "Paige Delancey"
        elif sV == "4":
            F_supervisor2 = "Max Konzerowsky"
        elif sV == "5":
            F_supervisor2 = "Jade"
        else:
            await channel.send("That's not a valid number! <1 - 5> (Ending the form...)")
            return


        embed = discord.Embed(title = "Q12-What is your role on each of the respective teams?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_role = await self.bot.wait_for('message', check=check)  

        embed = discord.Embed(title = "Q13-What type of confirmation does the organization you are submitting hours to require?" , description = "**EXAMPLE:**\nConfirmation E-mail, Signature from the company, etc.", color = 0x34eb71)
        await channel.send(embed = embed)
        F_confirmation = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q14-Describe what you did to earn your hours, (Please break it down into several tangible increments if possible)", color = 0x34eb71)
        await channel.send(embed = embed)
        F_howGetHour = await self.bot.wait_for('message', check=check)

        embed = discord.Embed(title = "Q15-Does your organization/college require an adult supervisors information?", color = 0x34eb71)
        await channel.send(embed = embed)
        F_needAdultInfo = await self.bot.wait_for('message', check=check)

        await givePDF(F_fullname.content, F_studentID.content, F_schoolName.content, F_schoolNumber.content, F_address.content, F_townANDcity.content, F_state.content, F_email.content, F_howGetHour.content, self, ctx.author.id, F_supervisor2)

        if F_supervisor2 == "Ethan Hsu":
            ID = 544724467709116457
        elif F_supervisor2 == "Jason Mei":
            ID = 229244813659209738
        elif F_supervisor2 == "Paige Delancey":
            ID = 392811824082583552
        elif F_supervisor2 == "Max Konzerowsky":
            ID = 450476337954553858
        #elif F_supervisor == "Shane":
            #ID = 690709453074464789
        elif F_supervisor2 == "Jade":
            ID = 644918892849790997
        else:
            return print("not a valid number")
            

        embed = discord.Embed(title = "That's it!", description = "Ready to submit?\n*React with the proper reaction!*\n✅ - SUBMIT\n❌ - CANCEL", color = 0x5ff5e6)
        embed.set_footer(text = "You have 150 seconds to react, otherwise the application will automatically cancel.")
        message = await channel.send(embed = embed)

        reactions = ['✅', '❌']
        for emoji in reactions:
            await message.add_reaction(emoji)

        def check2(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=150.0, check=check2)
            if str(reaction.emoji) == "❌":
                await channel.send("Ended Form...")
                await message.delete()
                return
            else:
                embed = discord.Embed(title = "Submitted PDF", description = "I have sent your PDF!", color = 0x5ff5e6)
                embed.add_field(name = "What To Do Next", value = f"Now that you have submitted your form, you must wait for your supervisor, {F_supervisor2}, to approve the request. Once they have done that you will receive another DM with your signed PDF.")
                await channel.send(embed = embed)

        except Exception as e:
            await channel.send(f"You didn't react in time! (Ending form.)\n{e}")

        #ID = 409152798609899530
        supervisor = await self.bot.fetch_user(ID)
        channel2 = await supervisor.create_dm()

        embed = discord.Embed(title = f"Requesting Authorization for {ctx.author.display_name}'s Community Service PDF!", description = f"The following user has requested for their {F_numHours.content} hours and you are required to sign this PDF if you approve of this. ", color = 0x5ff5e6)
        embed.add_field(name = "Approval", value = f"**By clicking on the “✅” below I, {F_supervisor2} confirm:\n(a) that {ctx.author.display_name} has done a total of {F_numHours.content} community service hours as a volunteer for School Simplified.\n(b) that {ctx.author.display_name} has received no compensation for the work described.\n(c) that I, {F_supervisor2}, consent to the release, storage and usage of my signature for the exclusive purpose of fulfilling {ctx.author.display_name}‘s community service hours performed for School Simplified.\n(d) that any other contracts or agreements which myself or my legal parent or guardian has signed shall supersede this agreement.**")
        embed.add_field(name = "Denial", value = "**If you do not agree with the following terms, then react with ❌ to deny their request.**", inline = False)
        embed.set_footer(text = f"Please REVIEW the PDF before you either accept or deny! | {ctx.author.id}")
        msg = await channel2.send(embed = embed)
        DiscID = ctx.author.id
        await channel2.send(file=discord.File(fr"PDF/rec-{DiscID}.pdf"))

        for emoji in reactions:
            await msg.add_reaction(emoji)



        embed = discord.Embed(title = f"Full Application", description = f"Viewing {ctx.author.mention}'s application.", color= 0x34eb71)
        embed.add_field(name = "Q1-What is your full name?", value = F_fullname.content)

        embed.add_field(name = "Q2-What is your email address?", value = F_email.content)

        embed.add_field(name = "Q3-What is your student ID number?", value = F_studentID.content)

        embed.add_field(name = "Q4-What is your home's street address?", value = F_address.content)

        embed.add_field(name = "Q5-In what city or town do you live in?", value = F_townANDcity.content)

        embed.add_field(name = "Q6-In what state do you live in?", value = F_state.content)

        embed.add_field(name = "Q7-What is the name of your school?", value = F_schoolName.content)

        embed.add_field(name = "Q8-What is the telephone number of your school?", value = F_schoolNumber.content)

        embed.add_field(name = "Q9-How many hours are you requesting?", value = F_numHours.content)

        embed.add_field(name = "Q10-How did you acquire your service hours?", value = F_hourAcquire.content)

        embed.add_field(name = "Q11-Who is your supervisor?", value = F_supervisor2)

        embed.add_field(name = "Q12-What is your role on each of the respective teams?", value = F_role.content)

        embed.add_field(name = "Q13-What type of confirmation does the organization you are submitting hours to require?", value = F_confirmation.content)

        embed.add_field(name = "Q14-Describe what you did to earn your hours, (Please break it down into several tangible increments if possible)", value = F_howGetHour.content)

        embed.add_field(name = "Q15-Does your organization/college require an adult supervisors information?", value = F_needAdultInfo.content)
        await channel2.send(embed = embed)

        

        






def setup(bot):
    bot.add_cog(CogCMD(bot))