import discord
import logging
from discord.ext import commands
from datetime import datetime
import asyncio
from pathlib import Path
import os
import subprocess
import time
import sys
import aiohttp
import traceback
from discord_slash import SlashCommand
from discord_slash import SlashContext

#Applying towards intents
intents = discord.Intents.default()  
intents.reactions = True
intents.members = True
intents.presences = True

#Defining client and SlashCommands
client = commands.Bot(command_prefix="&", intents=intents)
client.slash = SlashCommand(client, sync_commands=True) 
client.remove_command("help")


#Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
now = datetime.now().strftime("%H:%M:%S")

logger.info(f"PDFBOTv2 has started! {now}")


def get_extensions():  # Gets extension list dynamically
    extensions = []
    for file in Path("cogs").glob("**/*.py"):
        if "!" in file.name or "__" in file.name:
            continue
        extensions.append(str(file).replace("/", ".").replace(".py", ""))
    return extensions

async def force_restart(ctx):  #Forces REPL to apply changes to everything
    try:
        subprocess.run("python main.py", shell=True, text=True, capture_output=True, check=True)
    except Exception as e:
        await ctx.send(f"❌ Something went wrong while trying to restart the bot!\nThere might have been a bug which could have caused this!\n**Error:**\n{e}")
    finally:
        sys.exit(0)


 
@client.event
async def on_ready():
    print(discord.__version__)
    print("Current Time =", now)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"you get your Community Service Hours! | &form")) 



for ext in get_extensions():
    client.load_extension(ext)



@client.group(aliases=['cog'])
@commands.is_owner()
async def cogs(ctx):
    pass


@cogs.command()
@commands.is_owner()
async def unload(ctx, ext):
    if "cogs." not in ext:
        ext = f"cogs.{ext}"
    if ext in get_extensions():
        client.unload_extension(ext)
        embed = discord.Embed(
            title="Cogs - Unload", description=f"Unloaded cog: {ext}", color=0xd6b4e8)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Cogs Reloaded", description=f"Cog '{ext}' not found", color=0xd6b4e8)
        await ctx.send(embed=embed)


@cogs.command()
@commands.is_owner()
async def load(ctx, ext):
    if "cogs." not in ext:
        ext = f"cogs.{ext}"
    if ext in get_extensions():
        client.load_extension(ext)
        embed = discord.Embed(title="Cogs - Load",
                              description=f"Loaded cog: {ext}", color=0xd6b4e8)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Cogs - Load", description=f"Cog '{ext}' not found.", color=0xd6b4e8)
        await ctx.send(embed=embed)


@cogs.command(aliases=['restart'])
@commands.is_owner()
async def reload(ctx, ext):
    with open("commandcheck.txt", "w") as f:
        f.write("ON")
    if ext == "all":
        embed = discord.Embed(
            title="Cogs - Reload", description="Reloaded all cogs", color=0xd6b4e8)
        for extension in get_extensions():
            client.reload_extension(extension)
        await ctx.send(embed=embed)
        with open("commandcheck.txt", "w") as f:
            f.write("OFF")
        return

    if "cogs." not in ext:
        ext = f"cogs.{ext}"

    if ext in get_extensions():
        client.reload_extension(ext)
        embed = discord.Embed(
            title="Cogs - Reload", description=f"Reloaded cog: {ext}", color=0xd6b4e8)
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Cogs - Reload", description=f"Cog '{ext}' not found.", color=0xd6b4e8)
        await ctx.send(embed=embed)
    with open("commandcheck.txt", "w") as f:
        f.write("OFF")


@cogs.command()
@commands.is_owner()
async def view(ctx):
    msg = " ".join(get_extensions())
    embed = discord.Embed(title="Cogs - View", description=msg, color=0xd6b4e8)
    await ctx.send(embed=embed)

@client.command()
async def gitpull(ctx, mode = "-a"):
    output = ''
    typebot = "STABLE"
    if typebot == "STABLE":
        try:
            p = subprocess.run("git fetch --all", shell=True, text=True, capture_output=True, check=True)
            output += p.stdout
        except Exception as e:
            await ctx.send("⛔️ Unable to fetch the Current Repo Header!")
            await ctx.send(f"**Error:**\n{e}")
        try:
            p = subprocess.run("git reset --hard origin/main", shell=True, text=True, capture_output=True, check=True)
            output += p.stdout
        except Exception as e:
            await ctx.send("⛔️ Unable to apply changes!")
            await ctx.send(f"**Error:**\n{e}")
        embed = discord.Embed(title = "GitHub Local Reset", description = "Local Files changed to match PortalBot/Main", color = 0x3af250)
        embed.add_field(name = "Shell Output", value = f"```shell\n$ {output}\n```")
        embed.set_footer(text = "Attempting to restart the bot...")
        msg = await ctx.send(embed=embed)
        if mode == "-a":
            await force_restart(ctx)
        elif mode == "-c":
            await ctx.invoke(client.get_command('cogs reload'), ext='all') 



client.run(stuff)

