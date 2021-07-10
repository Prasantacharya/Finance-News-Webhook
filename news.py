import requests
import asyncio
import random
from bs4 import BeautifulSoup

# Headers so sites will accept the request
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
})

def getStockInfo(ticker, headers):
    # get ticker info from yahoo finance
    # the reason for the random.randint is because yahoo finance has 2 different endpoints, and we dont want to send too many to one
    url = f"https://query{random.randint(1,2)}.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    financeData = requests.get(url, headers=headers).json()["quoteResponse"]["result"][0]
    '''
        Gets this information that can be sent:
        ---
        - Stock name, daily range, market / post-market price
        - average analyst rating
        - footer saying take the analyst number with a grain of salt, and not financial advice
    '''
    print(financeData)

# getStockInfo("AMD", headers)

# gets the title of the article and a summary of the text
async def getSummary(headers, data):
    # make the request
    page = requests.get(data["link"], headers=headers)
    # using soup to parse the page 
    soup = BeautifulSoup(page.content, 'html5lib')
    
    title = soup.title.get_text()
    # this monstrosity makes a summary of the article.
    # summar is limited to 50 words
    text = ' '.join((' '.join(map(lambda item: item.get_text(), soup.find_all("p")))).split(' ')[:50]) + ' ...'
    return {"title":title, "text":text, "ticker": data["ticker"], "link": data['link']}

# Gets financial articles of note from google finance
# If an article talks about a ticker (stock or crypto) it will be gotten
def getPages(url, headers, tag, body):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html5lib") 
    articleBlock = soup.find(tag, body)
    
    flag = { "link": "", "ticker": []}
    articleArray = []
    for link in articleBlock.find_all('a'):
        linkLocation = link.get('href')
        
        if flag["link"] == linkLocation and len(flag["ticker"]) > 0:
            articleArray.append(flag)
            flag = {"link": "", "ticker": []}
        elif flag["link"] != linkLocation and linkLocation[0:4] == "http":
            flag["link"] = linkLocation
        elif linkLocation[0:4] != "http":
            flag["ticker"].append(linkLocation.split('/')[2])

    return articleArray

# driver function
async def driver(headers, relevantLinks):
    data = await asyncio.gather(*(getSummary(headers, link) for link in relevantLinks))
    for item in data:
        print(f"{item['ticker']} news: {item['link']}\n---\n{item['title']}\n{item['text']}\n")

# Gets the links from google finance 
relevantLinks = getPages("https://www.google.com/finance/", headers, "section", {"aria-labelledby": "news-title"})

asyncio.run(driver(headers, relevantLinks))
