import discord
import asyncio
from discord.ext import commands
import yaml

class Help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(asiases=["help", "man", "commands"])
    async def on_message(self, ctx):
        # make embed
        # get config
        embed = discord.Embed(
            title="Commands:",
            color="#CC790"
        )
        embed.set_author(
            name="Stonk Bot",
            url="https://github.com/Prasantacharya/Golden-Goose",
            icon_url="https://danbooru.donmai.us/data/original/3a/0a/__original_drawn_by_osananajimi_neko__3a0a2506756544b25584b7a4dd6b1f30.jpg"
        )
        
        # send embed
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
