import requests
import asyncio
import random
from bs4 import BeautifulSoup

def getStockInfo(ticker, headers):
    # get ticker info from yahoo finance
    # the reason for the random.randint is because yahoo finance has 2 different endpoints,
    # and we dont want to send too many to one
    url = f"https://query{random.randint(1,2)}.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    data = requests.get(url, headers=headers).json()["quoteResponse"]["result"][0]
    name = ""
    # check if `displayName` is there, else use shortName
    if "displayName" in data:
        name = data["displayName"]
    else:
        name = data["shortName"]
    change = data['regularMarketChangePercent']
    plus = ""
    if change > 0:
        plus = "+"
    return f"{name} ({plus}{change:.2f} %)"

# gets the title of the article and a summary of the text
async def getSummary(headers, data):
    # make the request
    page = requests.get(data["link"], headers=headers)
    # using soup to parse the page
    soup = BeautifulSoup(page.content, 'lxml')

    title = " ".join(soup.title.get_text().split())
    # This monstrosity gets the first few words of article (hopefully).
    # Essentially an intro that is limited to 30 words
    text = ' '.join((' '.join(map(lambda item: item.get_text(), soup.find_all("p")))).split()[:30]) + ' ...'
    return {"title":title, "text":text, "ticker": data["ticker"], "names": data["tickerNames"], "link": data['link']}

# Gets financial articles of note from google finance
# If an article talks about a ticker (stock or crypto) it will be gotten
def getPages(url, headers, tag, body):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    articleBlock = soup.find(tag, body)

    flag = { "link": "", "ticker": [], "tickerNames": []}
    articleArray = []
    for link in articleBlock.find_all('a'):
        linkLocation = link.get('href')

        if flag["link"] == linkLocation and len(flag["ticker"]) > 0:
            articleArray.append(flag)
            flag = {"link": "", "ticker": [], "tickerNames": []}
        elif flag["link"] != linkLocation and linkLocation[0:4] == "http":
            flag["link"] = linkLocation
        elif linkLocation[0:4] != "http":
            tickerName = linkLocation.split('/')[2].split(":")[0]
            # Dosent get stonks with '.' or other non-alphanumeric characters, with the exception of '-'
            # Did this cuz of an edge case with Berkshire Hathaway
            if not (tickerName.isalnum() or '-' in tickerName):
                continue

            flag["ticker"].append(tickerName)
            flag["tickerNames"].append(getStockInfo(tickerName, headers))
    return articleArray

# driver function
async def driver(headers, relevantLinks):
    data = await asyncio.gather(*(getSummary(headers, link) for link in relevantLinks))
    return data

def run():
    # Headers so sites will accept the request
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    })
    # Gets the links from google finance
    relevantLinks = getPages("https://www.google.com/finance/", headers, "section", {
        "aria-labelledby": "news-title"
    })
    return asyncio.run(driver(headers, relevantLinks))
