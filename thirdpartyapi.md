# Third-Party API Integration

## 📌 What is Third-Party API Integration?

Third-party API integration means using an API provided by another service or application inside our own application.

In this project, we are using the **JSONPlaceholder API** as a third-party API and connecting it with **FastAPI** using Python's `requests` library.

---

## 1. Importing Libraries

```python
import requests
from fastapi import FastAPI
```

### `requests`

The `requests` library is used to send HTTP requests to external APIs.

For example:

```python
requests.get(url)
```

sends a **GET request** to the given URL.

### `FastAPI`

`FastAPI` is used to create our own API and define endpoints.

---

## 2. Sending a Request to the Third-Party API

```python
response = requests.get("https://jsonplaceholder.typicode.com/posts")
```

Here, we send a **GET request** to the JSONPlaceholder API.

The URL:

```text
https://jsonplaceholder.typicode.com/posts
```

returns a list of posts.

The response from the external API is stored in the `response` variable.

---

## 3. Converting the Response to JSON

```python
data = response.json()
```

The API returns data in JSON format.

The `.json()` method converts the JSON response into Python data, usually a **list or dictionary**.

---

## 4. Printing the First Two Posts

```python
print(data[:2])
```

`data` contains all the posts.

Using:

```python
data[:2]
```

selects the first two posts from the list.

This is only used to check or view the data returned by the third-party API.

---

## 5. Creating the FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application.

The `app` object is used to define our API routes.

---

# 6. Get All Posts

```python
@app.get("/posts")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return response.json()
```

### `@app.get("/posts")`

This creates a **GET endpoint**:

```text
GET /posts
```

When a user visits:

```text
http://127.0.0.1:8000/posts
```

this function is executed.

### Function

```python
def get_posts():
```

This function handles the `/posts` request.

### API URL

```python
url = "https://jsonplaceholder.typicode.com/posts"
```

This is the URL of the third-party API.

### Sending the Request

```python
response = requests.get(url)
```

A GET request is sent to JSONPlaceholder.

### Returning the Data

```python
return response.json()
```

The response is converted to JSON and returned to the client.

So the flow is:

```text
Client
   ↓
FastAPI /posts
   ↓
requests.get()
   ↓
JSONPlaceholder API
   ↓
JSON response
   ↓
FastAPI
   ↓
Client
```

---

# 7. Get a Single Post

```python
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    return response.json()
```

This endpoint is used to get **one specific post**.

---

## Path Parameter

```python
@app.get("/posts/{post_id}")
```

`{post_id}` is a **path parameter**.

For example:

```text
/posts/1
/posts/5
/posts/10
```

Here, `1`, `5`, and `10` are different values of `post_id`.

---

## `post_id: int`

```python
def get_post(post_id: int):
```

This tells FastAPI that `post_id` should be an integer.

For example:

```text
/posts/5
```

is valid.

But:

```text
/posts/abc
```

is not valid because `abc` is not an integer.

---

## Creating the API URL Dynamically

```python
url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
```

The `f-string` inserts the value of `post_id` into the URL.

For example, if:

```python
post_id = 5
```

then the URL becomes:

```text
https://jsonplaceholder.typicode.com/posts/5
```

---

## Sending the Request

```python
response = requests.get(url)
```

A GET request is sent to the third-party API to retrieve that particular post.

---

## Returning the Response

```python
return response.json()
```

The response from JSONPlaceholder is converted into JSON and returned to the user.

---

# 🔄 Complete Flow

### Getting all posts

```text
Client
   ↓
GET /posts
   ↓
FastAPI
   ↓
requests.get(JSONPlaceholder)
   ↓
Third-Party API
   ↓
Posts data
   ↓
FastAPI
   ↓
Client
```

### Getting one post

For:

```text
GET /posts/1
```

the flow is:

```text
Client
   ↓
GET /posts/1
   ↓
FastAPI
   ↓
post_id = 1
   ↓
https://jsonplaceholder.typicode.com/posts/1
   ↓
Third-Party API
   ↓
Single post
   ↓
FastAPI
   ↓
Client
```

---

# 🧠 Key Concepts Used

| Concept           | Meaning                                         |
| ----------------- | ----------------------------------------------- |
| `requests`        | Python library for making HTTP requests         |
| `requests.get()`  | Sends a GET request                             |
| `FastAPI`         | Framework for creating APIs                     |
| `@app.get()`      | Creates a GET endpoint                          |
| `response.json()` | Converts API response into Python data          |
| `{post_id}`       | Path parameter                                  |
| `post_id: int`    | Specifies that the parameter must be an integer |
| JSONPlaceholder   | Third-party API used by our application         |

---

# ⭐ Main Idea

This project demonstrates **Third-Party API Integration**.

Our FastAPI application acts as an intermediary:

```text
Client → FastAPI → Third-Party API
                     ↓
Client ← FastAPI ← JSON Response
```

Instead of creating and storing the posts ourselves, our FastAPI application **requests the data from JSONPlaceholder and returns that data to the client**.
