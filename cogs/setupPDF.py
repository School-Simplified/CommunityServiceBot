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
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from core.common import add_opt
config, _ = load_config()


class CogCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def setup(self ,ctx, a1, a2 ,a3, a4, a5, a6):
        channel = ctx.channel
        author = ctx.author

        prompt_config(a1, "OrgName")
        prompt_config(a2, "OrgCity")
        prompt_config(a3, "OrgState")
        prompt_config(a4, "OrgPhone")
        prompt_config(a5, "OrgEmail")
        prompt_config(a6, "OrgContactName")
        await ctx.send(content = "Done!")

    @cog_ext.cog_slash(name="setupPDF", description = "Changes basic PDF info", guild_ids=[805593783684562965], options=add_opt)
    async def setupPDF(self ,ctx, a1, a2 ,a3, a4, a5, a6):
        channel = ctx.channel
        author = ctx.author

        prompt_config(a1, "OrgName")
        prompt_config(a2, "OrgCity")
        prompt_config(a3, "OrgState")
        prompt_config(a4, "OrgPhone")
        prompt_config(a5, "OrgEmail")
        prompt_config(a6, "OrgContactName")
        with open('Details.json', 'r') as content_file:
            content = content_file.read()

        await ctx.send(content = f"**I have saved your values!**\n\n```json\n{content}\n```")

def setup(bot):
    bot.add_cog(CogCMD(bot))