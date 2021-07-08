import discord
from discord.ext import commands

class stock(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(asiases=["stonk", "stock"])
    async def stockGet(self, ctx, arg):
        # first get yahoo finance data
        embed = discord.Embed(
            title=f'Stock:',
            description=""
        )
       await ctx.send(embed=embed)
