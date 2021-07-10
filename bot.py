import asyncio
import json
import os
import yaml
import discord
from discord.ext import commands

with open("config.yaml", 'r') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        sys.exit("Invalid config")

print("Successfully loaded config!\n")    

# bot token here
token = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix=config["prefix"])

print("loading cogs")
# add in the cogs here
for cog in config['cogs']:
    print(cog) # bot.load_extension("cogs." + config[cog]) 
    bot.load_extension(f"cogs.{cog}")

bot.run(config["token"])

