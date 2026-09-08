# FastAPI Pagination with Web Scraping

A simple FastAPI project that fetches text from the **Indian Express** website using `Requests` and `BeautifulSoup`.

This project also demonstrates the basic concept of **pagination** using `page` and `limit` query parameters.

---

## 📌 What is Pagination?

**Pagination** means dividing a large amount of data into smaller parts called **pages**.

For example, if an API has 100 items, instead of returning all 100 items at once, we can return 5 items per page.

```text
Page 1 → Items 1–5
Page 2 → Items 6–10
Page 3 → Items 11–15
Page 4 → Items 16–20
...
```

This makes APIs easier to use and reduces the amount of data returned in a single response.

---

## 🛠️ Technologies Used

* Python
* FastAPI
* Requests
* BeautifulSoup

---

## 📦 Installation

Install the required packages:

```bash
pip install fastapi uvicorn requests beautifulsoup4
```

---

## 💻 Code

```python
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

    # Find article links
    for item in soup.find_all("a"):
        text = item.get_text(strip=True)

        if text:
            titles.append(text)

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    return {
        "data": titles[start:end]
    }
```

---

# 🔍 Code Explanation

## 1. Import FastAPI

```python
from fastapi import FastAPI
```

This imports FastAPI so we can create our API.

---

## 2. Import Requests

```python
import requests
```

`requests` is used to send an HTTP request to the Indian Express website.

```python
response = requests.get(url, headers=headers)
```

This downloads the webpage.

---

## 3. Import BeautifulSoup

```python
from bs4 import BeautifulSoup
```

BeautifulSoup is used to read and extract information from HTML.

```python
soup = BeautifulSoup(response.text, "html.parser")
```

Here, the HTML response is converted into a BeautifulSoup object.

---

# 📰 Extracting Data

We create an empty list:

```python
titles = []
```

Then we find all `<a>` tags:

```python
for item in soup.find_all("a"):
```

We extract the text:

```python
text = item.get_text(strip=True)
```

If the text exists, we add it to the list:

```python
if text:
    titles.append(text)
```

Now `titles` contains the scraped text.

---

# 📄 Pagination

The endpoint accepts two query parameters:

```python
def get_news(page: int = 1, limit: int = 5):
```

### `page`

`page` tells the API **which page we want**.

Default:

```text
page = 1
```

### `limit`

`limit` tells the API **how many items should be returned on each page**.

Default:

```text
limit = 5
```

---

# 🧮 Pagination Formula

The important part is:

```python
start = (page - 1) * limit
end = start + limit
```

These values determine which items should be returned.

---

## Example 1: Page 1

Suppose:

```text
page = 1
limit = 5
```

Calculation:

```text
start = (1 - 1) * 5
      = 0

end = 0 + 5
    = 5
```

So:

```python
titles[0:5]
```

returns the first 5 items.

```text
Items 1–5
```

---

## Example 2: Page 2

Suppose:

```text
page = 2
limit = 5
```

Calculation:

```text
start = (2 - 1) * 5
      = 5

end = 5 + 5
    = 10
```

So:

```python
titles[5:10]
```

returns:

```text
Items 6–10
```

---

## Example 3: Page 3

Suppose:

```text
page = 3
limit = 5
```

Calculation:

```text
start = (3 - 1) * 5
      = 10

end = 10 + 5
    = 15
```

So:

```python
titles[10:15]
```

returns:

```text
Items 11–15
```

---

# 🔗 API Requests

### Page 1

```text
/news?page=1&limit=5
```

Returns:

```text
Items 1–5
```

### Page 2

```text
/news?page=2&limit=5
```

Returns:

```text
Items 6–10
```

### Page 3

```text
/news?page=3&limit=5
```

Returns:

```text
Items 11–15
```

You can change the number of items per page:

```text
/news?page=1&limit=10
```

This returns the first 10 items.

---

# ✂️ Python List Slicing

The final data is returned using:

```python
titles[start:end]
```

This is called **list slicing**.

For example:

```python
titles[0:5]
```

means:

```text
Start from index 0
Stop before index 5
```

So it returns:

```text
Index: 0  1  2  3  4
       ↓  ↓  ↓  ↓  ↓
       1  2  3  4  5
```

Python does not include the ending index.

Therefore:

```python
titles[5:10]
```

means:

```text
Index: 5  6  7  8  9
       ↓  ↓  ↓  ↓  ↓
       6  7  8  9  10
```

---

# 📤 API Response

The API returns:

```json
{
    "data": [
        "News headline 1",
        "News headline 2",
        "News headline 3",
        "News headline 4",
        "News headline 5"
    ]
}
```

The actual headlines will depend on the data currently available on the website.

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Open the news endpoint:

```text
http://127.0.0.1:8000/news
```

---

# 📚 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can enter different values for:

* `page`
* `limit`

and test pagination directly from Swagger UI.

---

# 🧠 Pagination Flow

```text
Client
  ↓
GET /news?page=2&limit=5
  ↓
Scrape News Data
  ↓
Calculate start and end
  ↓
start = (2 - 1) × 5 = 5
end = 5 + 5 = 10
  ↓
titles[5:10]
  ↓
Return Items 6–10
```

---

# 🎯 Key Learning

This project demonstrates:

* Creating a FastAPI GET endpoint
* Using query parameters
* Web scraping with Requests
* Parsing HTML with BeautifulSoup
* Python list slicing
* Implementing basic pagination

### Main Pagination Logic

```python
start = (page - 1) * limit
end = start + limit

data = titles[start:end]
```

**In simple words:**

> `page` tells us **which page** to get, while `limit` tells us **how many items** to show on that page.
