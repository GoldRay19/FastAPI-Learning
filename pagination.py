from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/news")
def get_news(page: int = 1, limit: int = 5):

    url = "https://indianexpress.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    titles = []

    # Try finding article links
    for item in soup.find_all("a"):
        text = item.get_text(strip=True)

        if text:
            titles.append(text)

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    return {
        "data": titles[:5]
    }