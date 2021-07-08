import asyncio
import json
import os
import yaml
import discord
from discord.ext import commands

def run():
    # gets the config file
    with open("config.yaml", 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print("Could not load config")
            return
    print("Successfully loaded config!\n")    
    # bot token here
    token = os.getenv('DISCORD_BOT_TOKEN')
    print(f"token: {token}")
    print(config["prefix"])
    bot = commands.Bot(command_prefix=config["prefix"])
    # add in the cogs here
    for cog in config['cogs']:
        print(cog) # bot.load_extension("cogs." + config[cog]) 
    bot.load_extension("cogs.help")
    bot.run("ODA1NTM3ODAwMTkxMDgyNTA2.YBcViQ.QWuXr4xfLgO8JZhHzroUbU-oxBA")
    print("exiting")


if __name__ == '__main__':
    # parse the config file
    run()
