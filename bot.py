import os
import discord
from discord import user
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv
import json
from loggingChannel import sendLog
from re import search
import csv
import os.path
from os import path
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

myid = '<@849728637266952193>'
bot = commands.Bot(command_prefix="..", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [786690956514426910, 254779349352448001]  # Put your server ID in this array.


async def updateStatus():
    with open('status.json') as fs:
        data = json.load(fs)
    await client.change_presence(
        activity=await activityType(data))


async def activityType(data):
    if data["activity"]["type"] == "PLAYING":
        return discord.Activity(type=discord.Game(data["activity"]["name"]))
    elif data["activity"]["type"] == "STREAMING":
        return discord.Activity(activity=discord.Streaming(name=data["activity"]["name"], url=data["activity"]["url"]))
    elif data["activity"]["type"] == "WATCHING":
        return discord.Activity(type=discord.ActivityType.watching, name=data["activity"]["name"])
    elif data["activity"]["type"] == "LISTENING":
        return discord.Activity(type=discord.ActivityType.listening, name=data["activity"]["name"])


@client.event
async def on_ready():
    # Loaded
    print(await sendLog(log=(f'I live'), client=client))
    await updateStatus()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel

    # Update Status
    await updateStatus()

    if path.exists(f'./scripts/{message.channel.name} - {message.channel.id}.csv'):
        if len(message.content) > 0:
            if not (search("\.gif", message.content.lower()) or search("http", message.content.lower())):
                now = datetime.datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M:%S")
                with open(f'./scripts/{message.channel.name} - {message.channel.id}.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([date_time, message.content, message.author.name])

    # Log message
    print(f'{message.author.name} sent: {message.content} on Channel: {channel.id}')

    # Store Mentions if Any
    mentions = message.mentions

    # Check if asked to quit
    if len(mentions) > 0:
        if mentions[0].id == 849728637266952193:
            if search("^!quit", message.content.lower()) and message.channel == client.get_channel(789190323326025789):
                await client.logout()


# ======================================== SLASH COMMANDS ========================================

@slash.slash(name="record_here", description="Starts recording channel.", guild_ids=guild_ids)
async def record_here(ctx):
    if not path.exists(f'./scripts/{ctx.channel.name} - {ctx.channel.id}.csv'):
        with open(f'./scripts/{ctx.channel.name} - {ctx.channel.id}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "dialogue", "person"])
        await ctx.send(f"Started recording {ctx.channel.name}")
    else:
        await ctx.send(f"Already recording {ctx.channel.name}")


client.run(TOKEN)
