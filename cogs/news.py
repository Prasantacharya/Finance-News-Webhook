import requests
import asyncio
from bs4 import BeautifulSoup

# Headers so sites will accept the request
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
})

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
    
    flag = { "include": False, "ticker:": ""}
    articleArray = []
    for link in articleBlock.find_all('a'):
        linkLocation = link.get('href')
        if flag["include"]:
            articleArray.append({ "ticker": flag["ticker"], "link": linkLocation})
        
        if linkLocation[0:4] != "http":
            flag["include"] = True
            flag["ticker"] = linkLocation.split('/')[2]
        else:
            flag["include"] = False
    return articleArray

# driver function
async def driver(headers, relevantLinks):
    data = await asyncio.gather(*(getSummary(headers, link) for link in relevantLinks))
    for item in data:
        print(f"{item['ticker']} news: {item['link']}\n---\n{item['title']}\n{item['text']}\n")

# Gets the links from google finance 
relevantLinks = getPages("https://www.google.com/finance/", headers, "section", {"aria-labelledby": "news-title"})

# asyncio.run(driver(headers, relevantLinks))
