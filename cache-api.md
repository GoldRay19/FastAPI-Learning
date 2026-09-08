# FastAPI Caching with TTL

A simple FastAPI project demonstrating **caching** and **TTL (Time To Live)** using Hacker News data.

## 📌 What is Caching?

Caching means storing fetched data temporarily so it can be reused instead of making the same request again.

In this project:

* First request → Fetches fresh data
* Next requests → Uses cached data
* Cache expires after the TTL
* After expiration → Fetches fresh data again

## ⏱️ What is TTL?

**TTL (Time To Live)** defines how long the cached data remains valid.

```python
TTL = 60
```

This means the cache will remain valid for **60 seconds**.

You can change it:

```python
TTL = 30      # 30 seconds
TTL = 300     # 5 minutes
TTL = 3600    # 1 hour
```

## 💻 Code

```python
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI()

# Cache Storage
cache_data = []
last_fetch = 0

# TTL Configuration
TTL = 60


@app.get("/news")
def get_news():

    global cache_data, last_fetch

    start = time.time()

    # Check if cache has expired
    if time.time() - last_fetch > TTL:

        print("Fetching Fresh Data")

        url = "https://news.ycombinator.com/"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        cache_data = [
            item.text
            for item in soup.find_all("span", class_="titleline")
        ]

        # Update last fetch time
        last_fetch = time.time()

    else:

        print("Using Cache Data")

    end = time.time()

    time_taken = round(end - start, 4)

    print("Time Taken:", time_taken)

    return {
        "time_taken": time_taken,
        "ttl": TTL,
        "data": cache_data[:5]
    }
```

## 🔄 How It Works

### First Request

```text
Fetching Fresh Data
```

The application fetches data from Hacker News and stores it in:

```python
cache_data
```

It also stores the time when the data was fetched:

```python
last_fetch = time.time()
```

### Request Within TTL

```text
Using Cache Data
```

The application uses the cached data instead of sending another request.

### After TTL Expires

The condition:

```python
time.time() - last_fetch > TTL
```

becomes `True`.

The application fetches fresh data and updates the cache.

## 📊 Example

First request:

```text
Fetching Fresh Data
Time Taken: 0.75
```

Second request within 60 seconds:

```text
Using Cache Data
Time Taken: 0.0001
```

The cached request is faster because no external request is made.

## 🔑 Important Variables

### Cache Storage

```python
cache_data = []
```

Stores the fetched data.

### Last Fetch Time

```python
last_fetch = 0
```

Stores when the data was last fetched.

### TTL

```python
TTL = 60
```

Defines how long the cache remains valid.

### Expiration Check

```python
if time.time() - last_fetch > TTL:
```

Checks whether the cache has expired.

## ▶️ Run

Install dependencies:

```bash
pip install fastapi uvicorn requests beautifulsoup4
```

Run the application:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/news
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 🎯 Key Learning

**Caching** stores and reuses data, while **TTL** determines how long that cached data remains valid.

```text
Request
   ↓
Cache exists?
   ↓
 ┌───────┴───────┐
Yes              No / Expired
 ↓                  ↓
Use Cache       Fetch Fresh Data
 ↓                  ↓
Return Data      Update Cache
```
