# Web Scraping with FastAPI

## 📌 What is Web Scraping?

**Web scraping** is the process of extracting information from a website automatically using a program.

In this project, we use:

* **FastAPI** → to create our API
* **Requests** → to send a request to the website
* **BeautifulSoup** → to extract specific information from the HTML
* **Indian Express** → the website from which we extract news titles

---

## 1. Importing Libraries

```python
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
```

### `FastAPI`

FastAPI is used to create our API and define API endpoints.

### `requests`

The `requests` library is used to send HTTP requests to websites.

For example:

```python
requests.get(url)
```

sends a GET request to the specified URL.

### `BeautifulSoup`

BeautifulSoup is used to **parse HTML** and extract specific elements from a webpage.

---

## 2. Creating the FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application.

The `app` object is then used to create API routes.

---

# 3. Creating the `/news` Endpoint

```python
@app.get("/news")
def get_news():
```

This creates a **GET endpoint**:

```text
GET /news
```

When a client sends a GET request to:

```text
http://127.0.0.1:8000/news
```

the `get_news()` function is executed.

> **Important:** `@app.egt("/news")` in the original code is a typo. It should be `@app.get("/news")`.

---

# 4. Website URL

```python
url = "https://indianexpress.com/"
```

This is the URL of the website that we want to scrape.

---

# 5. Sending a Request to the Website

```python
response = requests.get(url)
```

The `requests.get()` function sends an HTTP GET request to the website.

The HTML response returned by the website is stored in:

```python
response
```

---

# 6. Parsing the HTML

```python
soup = BeautifulSoup(response.text, "html.parser")
```

Here:

### `response.text`

Contains the HTML source code received from the website.

### `BeautifulSoup()`

BeautifulSoup parses the HTML so that we can easily search for specific elements.

### `"html.parser"`

This tells BeautifulSoup to use Python's built-in HTML parser.

So:

```python
BeautifulSoup(response.text, "html.parser")
```

means:

> Take the HTML received from the website and parse it so we can extract information from it.

---

# 7. Creating a List for News Titles

```python
title = []
```

An empty list is created to store the news titles that we extract from the webpage.

---

# 8. Finding News Elements

```python
for item in soup.find_all("a", class_="topblockNews_sidebarLink"):
```

This is the main part of the web scraping process.

### `soup.find_all()`

`find_all()` searches the HTML for all elements matching the specified conditions.

We are looking for:

```html
<a class="topblockNews_sidebarLink">
```

The first argument:

```python
"a"
```

means we are searching for HTML `<a>` (anchor/link) elements.

The second argument:

```python
class_="topblockNews_sidebarLink"
```

means we only want `<a>` elements whose CSS class is:

```text
topblockNews_sidebarLink
```

The `class_` is written with an underscore because `class` is a reserved keyword in Python.

---

# 9. Extracting the Text

```python
title.append(item.text)
```

For every matching HTML element, `item.text` extracts the text inside that element.

For example, if the HTML contains:

```html
<a class="topblockNews_sidebarLink">
    India announces new policy
</a>
```

then:

```python
item.text
```

will give:

```text
India announces new policy
```

That text is then added to the `title` list.

---

# 10. Returning the News

```python
return {
    "news": title[:5]
}
```

The extracted news titles are returned as a JSON response.

### `title[:5]`

This selects only the **first five** items from the list.

For example, if the list contains:

```python
[
    "News 1",
    "News 2",
    "News 3",
    "News 4",
    "News 5",
    "News 6"
]
```

then:

```python
title[:5]
```

returns:

```python
[
    "News 1",
    "News 2",
    "News 3",
    "News 4",
    "News 5"
]
```

---

# 🔄 Complete Flow

```text
Client
   ↓
GET /news
   ↓
FastAPI
   ↓
requests.get()
   ↓
Indian Express Website
   ↓
HTML Response
   ↓
BeautifulSoup
   ↓
Find <a> elements with specific class
   ↓
Extract News Titles
   ↓
Take First 5 Titles
   ↓
Return JSON Response
   ↓
Client
```

---

# 🧠 Important Concepts

| Concept          | Meaning                                             |
| ---------------- | --------------------------------------------------- |
| Web Scraping     | Automatically extracting information from a website |
| `requests`       | Sends HTTP requests                                 |
| `requests.get()` | Sends a GET request                                 |
| `BeautifulSoup`  | Parses HTML                                         |
| `response.text`  | HTML content received from the website              |
| `html.parser`    | HTML parser used by BeautifulSoup                   |
| `find_all()`     | Finds all matching HTML elements                    |
| `class_`         | Searches for an HTML CSS class                      |
| `item.text`      | Extracts text from an HTML element                  |
| `append()`       | Adds an item to a list                              |
| `[:5]`           | Selects the first five items                        |
| FastAPI          | Creates the `/news` API endpoint                    |

---

# 📌 Complete Code

```python
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/news")
def get_news():
    url = "https://indianexpress.com/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = []

    for item in soup.find_all("a", class_="topblockNews_sidebarLink"):
        title.append(item.text)

    return {
        "news": title[:5]
    }
```

## ⭐ Main Idea

This project combines **web scraping and FastAPI**.

BeautifulSoup extracts information from the webpage, while FastAPI exposes that extracted information through our own API endpoint:

```text
Website → BeautifulSoup → FastAPI → Client
```

So instead of directly opening the website, a client can request:

```text
GET /news
```

and receive the extracted news titles as JSON.
