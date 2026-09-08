# import requests
# from bs4 import BeautifulSoup
# url="http://example.com"
# response=requests.get(url)
# soup=BeautifulSoup(requests.text,"html.parse")
# print(soup.title.text)

from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
app=FastAPI()
@app.egt("/news")
def get_news():
    url=""
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    title=[]
    for item in soup.find_all("a",class_="topblockNews_sidebarLink"):
        title.append(item.text)
    return {
        "news":title[:5]
    }
