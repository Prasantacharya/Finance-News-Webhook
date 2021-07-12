from discord_webhook import DiscordEmbed, DiscordWebhook
import requests
from time import sleep
import sys
import news # not a pip library, file that gets the articles, etc

# get what webhooks to send it too from the config file
# will warn if you do not have the config, and exit
try:
    from config import urls
except:
    sys.exit("Config was not loaded")

# get the articles
article = news.run()

webHook = DiscordWebhook(url=urls)

embed = DiscordEmbed(title='Finance News:', color='7289DA')

embed.set_footer(text='Articles were scraped from Google Finance • This is not financial advice\nStar us on Github! • https://github.com/Prasantacharya/Finance-News-Webhook')

for page in article:
    embedTitle = ', '.join(page["names"]) + " news:"
    embedText = f"[**{page['title']}**]({page['link']})\n{page['text']}"
    embed.add_embed_field(
        name=embedTitle,
        value=embedText,
        inline=False)

webHook.add_embed(embed)

resp = webHook.execute()
