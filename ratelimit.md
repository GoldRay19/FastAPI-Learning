# FastAPI Rate Limiting with SlowAPI

A simple **FastAPI** project demonstrating **Rate Limiting** using the **SlowAPI** library.

---

## 📌 What is Rate Limiting?

**Rate limiting** controls how many requests a client can make to an API within a specific amount of time.

For example:

```text
5 requests / minute
```

means a client can make a maximum of **5 requests in one minute**.

If the client makes more than 5 requests within that minute, the API returns:

```text
429 Too Many Requests
```

---

# 🤔 Why is Rate Limiting Important?

Without rate limiting, a client could send a large number of requests to an API.

For example:

```text
Client
  ↓
Request
Request
Request
Request
Request
Request
Request
Request
...
```

This can:

* Increase server load
* Slow down the API
* Consume unnecessary resources
* Cause abuse of the API
* Lead to excessive requests to external services

Rate limiting helps control this.

---

# 🔄 How Rate Limiting Works

In this project, we allow:

```text
5 requests per minute
```

The flow is:

```text
             Client
                ↓
           GET /data
                ↓
       Check Request Limit
                ↓
        ┌───────┴───────┐
        ↓               ↓
   ≤ 5 requests     > 5 requests
        ↓               ↓
     Success       429 Error
        ↓
   Return Data
```

---

# 🐌 What is SlowAPI?

**SlowAPI** is a rate-limiting library that can be used with FastAPI.

It allows us to easily define limits such as:

```python
@limiter.limit("5/minute")
```

Other examples include:

```python
@limiter.limit("10/minute")
```

```python
@limiter.limit("100/hour")
```

```python
@limiter.limit("1000/day")
```

---

# 📦 Installation

Install FastAPI, Uvicorn, and SlowAPI:

```bash
pip install fastapi uvicorn slowapi
```

---

# 💻 Code

```python
from fastapi import FastAPI, Request

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from fastapi.responses import JSONResponse


app = FastAPI()


# Limiter Setup
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter


# Error Handler
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):

    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many Requests"
        }
    )


# Rate Limited API
@app.get("/data")
@limiter.limit("5/minute")
def get_data(request: Request):

    return {
        "message": "Success"
    }
```

---

# 🔍 Code Explanation

## 1. Import FastAPI

```python
from fastapi import FastAPI, Request
```

`FastAPI` is used to create the API.

`Request` represents the incoming HTTP request.

The `Request` object is also required by SlowAPI for the rate limiter.

---

# 2. Import SlowAPI Limiter

```python
from slowapi import Limiter
```

`Limiter` is used to create the rate limiter.

It allows us to define limits such as:

```text
5 requests/minute
10 requests/minute
100 requests/hour
```

---

# 3. Get Client IP Address

```python
from slowapi.util import get_remote_address
```

`get_remote_address` is used to identify the client making the request.

In this example, the client's **IP address** is used as the rate-limit key.

This means different clients can have separate limits.

For example:

```text
Client A → 5 requests/minute
Client B → 5 requests/minute
```

The requests are tracked separately.

---

# 4. Import Rate Limit Error

```python
from slowapi.errors import RateLimitExceeded
```

`RateLimitExceeded` is the exception raised when a client exceeds the configured rate limit.

For example:

```text
Allowed → 5 requests
6th request → RateLimitExceeded
```

---

# 5. Import JSONResponse

```python
from fastapi.responses import JSONResponse
```

`JSONResponse` allows us to return a custom JSON response with a specific HTTP status code.

---

# 🚀 Create FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application.

---

# 🛡️ Limiter Setup

```python
limiter = Limiter(key_func=get_remote_address)
```

Here we create the rate limiter.

The important part is:

```python
key_func=get_remote_address
```

It tells SlowAPI to identify clients using their remote IP address.

---

# 🔗 Attach Limiter to FastAPI

```python
app.state.limiter = limiter
```

This attaches the limiter to the FastAPI application.

Now SlowAPI can use the limiter for our API routes.

---

# ⚠️ Error Handler

```python
@app.exception_handler(RateLimitExceeded)
```

This tells FastAPI:

> Whenever a `RateLimitExceeded` exception occurs, use this function to handle it.

The function is:

```python
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
```

---

# 🔴 HTTP 429 Response

Inside the error handler:

```python
return JSONResponse(
    status_code=429,
    content={
        "detail": "Too many Requests"
    }
)
```

The status code:

```text
429
```

means:

> **Too Many Requests**

The API response will look like:

```json
{
    "detail": "Too many Requests"
}
```

---

# 🌐 Create API Endpoint

```python
@app.get("/data")
```

This creates a GET endpoint:

```text
/data
```

The complete URL when running locally is:

```text
http://127.0.0.1:8000/data
```

---

# ⏱️ Apply Rate Limit

The most important line is:

```python
@limiter.limit("5/minute")
```

This means:

> Allow a maximum of 5 requests per minute.

So:

```text
Request 1 → Success
Request 2 → Success
Request 3 → Success
Request 4 → Success
Request 5 → Success
Request 6 → 429 Error
```

---

# 📌 Why `request` is Required

Our endpoint contains:

```python
def get_data(request: Request):
```

The `request` object represents the incoming HTTP request.

SlowAPI uses it while applying the rate limit.

Therefore, when using:

```python
@limiter.limit("5/minute")
```

keep the `Request` parameter in the endpoint.

---

# 🧪 Testing the API

Start the application:

```bash
uvicorn ratelimit:app --reload
```

If your Python file has a different name, replace `ratelimit` with your filename.

For example, if the file is:

```text
main.py
```

run:

```bash
uvicorn main:app --reload
```

---

# 🌐 Open the API

Open:

```text
http://127.0.0.1:8000/data
```

The first five requests should return:

```json
{
    "message": "Success"
}
```

After exceeding the limit, you should receive:

```json
{
    "detail": "Too many Requests"
}
```

with HTTP status:

```text
429
```

---

# 📚 Swagger UI

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Find:

```text
GET /data
```

Click:

```text
Try it out
```

Then:

```text
Execute
```

You can repeatedly execute the endpoint to test the rate limit.

---

# 🔢 Rate Limit Examples

## 5 Requests Per Minute

```python
@limiter.limit("5/minute")
```

Maximum:

```text
5 requests
```

within one minute.

---

## 10 Requests Per Minute

```python
@limiter.limit("10/minute")
```

Maximum:

```text
10 requests
```

within one minute.

---

## 100 Requests Per Hour

```python
@limiter.limit("100/hour")
```

Maximum:

```text
100 requests
```

within one hour.

---

## 1000 Requests Per Day

```python
@limiter.limit("1000/day")
```

Maximum:

```text
1000 requests
```

within one day.

---

# 📊 Example

Suppose we have:

```python
@limiter.limit("5/minute")
```

A client makes requests:

| Request | Result    |
| ------- | --------- |
| 1       | ✅ Success |
| 2       | ✅ Success |
| 3       | ✅ Success |
| 4       | ✅ Success |
| 5       | ✅ Success |
| 6       | ❌ 429     |
| 7       | ❌ 429     |

Once the rate-limit window resets, requests can be made again.

---

# 🧠 Simple Example

Imagine an API is a restaurant.

The restaurant can serve only:

```text
5 customers per minute
```

If more customers arrive:

```text
Customer 1 → Allowed
Customer 2 → Allowed
Customer 3 → Allowed
Customer 4 → Allowed
Customer 5 → Allowed
Customer 6 → Wait / Rejected
```

Rate limiting works in a similar way.

It prevents the server from receiving too many requests at once.

---

# 🔐 Rate Limiting and IP Addresses

This project uses:

```python
get_remote_address
```

Therefore, SlowAPI uses the client's IP address to identify clients.

For example:

```text
192.168.1.10 → 5 requests/minute
192.168.1.20 → 5 requests/minute
```

Each IP can have its own limit.

---

# ⚠️ Important Note

The rate limit:

```python
@limiter.limit("5/minute")
```

is applied to the endpoint where the decorator is placed.

For example:

```python
@app.get("/data")
@limiter.limit("5/minute")
def get_data(request: Request):
```

Only `/data` has this particular limit.

You can apply different limits to different endpoints:

```python
@app.get("/data")
@limiter.limit("5/minute")
def get_data(request: Request):
    return {"message": "Data"}
```

```python
@app.get("/users")
@limiter.limit("10/minute")
def get_users(request: Request):
    return {"message": "Users"}
```

---

# 🛠️ Common Rate Limit Formats

Some common formats are:

```text
5/minute
10/minute
100/hour
1000/day
```

The general idea is:

```text
<number>/<time period>
```

For example:

```python
"5/minute"
```

means:

```text
5 requests
    ↓
per minute
```

---

# 🔄 Complete Flow

```text
              Client
                 ↓
          GET /data
                 ↓
       SlowAPI Rate Limiter
                 ↓
       Identify Client IP
                 ↓
       Count Requests
                 ↓
        ┌────────┴────────┐
        ↓                 ↓
    Within Limit       Limit Exceeded
        ↓                 ↓
    API Executes       Raise Error
        ↓                 ↓
   Return Success       HTTP 429
```

---

# 🎯 Key Learning

### Rate Limiting

Controls how many requests a client can make within a specific time period.

### SlowAPI

Provides rate-limiting functionality for FastAPI applications.

### `get_remote_address`

Identifies the client using its remote IP address.

### `@limiter.limit()`

Defines the request limit.

Example:

```python
@limiter.limit("5/minute")
```

### HTTP 429

Indicates:

```text
Too Many Requests
```

---

# 📌 In One Line

> **Rate limiting protects an API by restricting how many requests a client can make within a specific time period.**

---

## 🚀 Project Structure

A simple project structure can be:

```text
FastApi-Learning/
│
├── ratelimit.py
└── ratelimit.md
```

Run the application with:

```bash
uvicorn ratelimit:app --reload
```

Then test:

```text
http://127.0.0.1:8000/data
```

or use Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 🎓 Final Summary

This project demonstrates how to add **rate limiting to a FastAPI endpoint using SlowAPI**.

The important parts are:

```python
limiter = Limiter(key_func=get_remote_address)
```

creates the limiter.

```python
app.state.limiter = limiter
```

connects it to FastAPI.

```python
@limiter.limit("5/minute")
```

allows only 5 requests per minute.

And:

```python
status_code=429
```

returns the appropriate response when the limit is exceeded.
