import asyncio
import json
import os
import yaml
import discord
from discord.ext import commands

async def run():
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
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=config["prefix"], intents=intents)
    
    try:
        # add in the cogs here
        for cog in config['cogs']:
            print(cog) # bot.load_extension("cogs." + config[cog]) 
        bot.load_extension("cogs.help")
        
        bot.run(token)
    except KeyboardInterrupt:
        await bot.close()
    
    print("exiting")


if __name__ == '__main__':
    # parse the config file
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    loop.run_until_complete(run())   
