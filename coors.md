# FastAPI CORS

## 1. What is CORS?

**CORS** stands for **Cross-Origin Resource Sharing**.

It is a browser security mechanism that controls whether a frontend running on one origin is allowed to make requests to a backend running on another origin.

For example, suppose:

```text
Frontend:
http://localhost:5173

Backend:
http://127.0.0.1:8000
```

These are different origins.

If the frontend tries to call the FastAPI backend:

```javascript
fetch("http://127.0.0.1:8000/home")
```

the browser may block the request unless the backend explicitly allows the frontend origin.

CORS is used to tell the browser:

> "This frontend is allowed to communicate with my backend."

---

# 2. What is an Origin?

An **origin** consists of three things:

```text
Protocol + Domain/Host + Port
```

For example:

```text
http://localhost:5173
```

contains:

```text
Protocol → http
Host     → localhost
Port     → 5173
```

Changing any of these makes it a different origin.

For example:

```text
http://localhost:5173
http://localhost:3000
http://127.0.0.1:5173
https://localhost:5173
```

are different origins.

---

# 3. Why is CORS required in FastAPI?

A common development setup is:

```text
React / Vite
     |
     | HTTP Request
     ↓
FastAPI
```

For example:

```text
React:
http://localhost:5173

FastAPI:
http://localhost:8000
```

The browser sees these as different origins.

Without CORS configuration, the browser can reject the request.

With CORS enabled, FastAPI can send the appropriate CORS headers allowing the request.

---

# 4. Import FastAPI

```python
from fastapi import FastAPI
```

This imports the `FastAPI` class.

We use it to create our backend application.

---

# 5. Import CORSMiddleware

```python
from fastapi.middleware.cors import CORSMiddleware
```

`CORSMiddleware` is middleware provided by FastAPI/Starlette for handling CORS.

Middleware is code that runs between the incoming request and your application.

The flow becomes:

```text
Client
   ↓
CORS Middleware
   ↓
FastAPI Application
   ↓
Route
   ↓
Response
```

---

# 6. Create the FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application instance.

We use `app` to define routes and configure the application.

For example:

```python
@app.get("/home")
def home():
    ...
```

---

# 7. Define Allowed Origins

```python
origins = ["http://localhost:5173"]
```

This defines which frontend origins are allowed to communicate with our backend.

Here we are allowing:

```text
http://localhost:5173
```

This is commonly the default development address for a Vite frontend.

For example, if your React/Vite application runs at:

```text
http://localhost:5173
```

then this origin should be included.

---

# 8. Why use a List?

`allow_origins` expects a list of allowed origins.

For example:

```python
origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]
```

Now both frontends are allowed:

```text
http://localhost:5173
http://localhost:3000
```

You can also include a deployed frontend:

```python
origins = [
    "http://localhost:5173",
    "https://example.com"
]
```

---

# 9. Add CORS Middleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

This adds CORS handling to the FastAPI application.

Let's understand each option.

---

# 10. `CORSMiddleware`

```python
CORSMiddleware
```

This tells FastAPI to use the CORS middleware.

It automatically handles CORS-related request and response headers.

---

# 11. `allow_origins`

```python
allow_origins=origins
```

This specifies which origins are allowed.

Since we defined:

```python
origins = ["http://localhost:5173"]
```

the frontend at:

```text
http://localhost:5173
```

is allowed to communicate with the backend.

---

# 12. `allow_credentials`

```python
allow_credentials=True
```

This allows credentials to be included in cross-origin requests.

Credentials can include things such as:

* Cookies
* Authorization-related credentials
* Browser credentials

For example, if your application uses authentication cookies, credentials may be required.

Example:

```python
allow_credentials=True
```

means the server allows credentialed cross-origin requests.

### Important

When using credentials, you should specify actual allowed origins rather than using:

```python
allow_origins=["*"]
```

A specific origin is safer and is required for credentialed browser requests.

---

# 13. `allow_methods`

```python
allow_methods=["*"]
```

This controls which HTTP methods are allowed.

The `*` means all methods.

Common HTTP methods include:

```text
GET
POST
PUT
PATCH
DELETE
OPTIONS
```

For example:

```python
allow_methods=["GET", "POST"]
```

would only allow GET and POST methods.

Using:

```python
allow_methods=["*"]
```

allows all HTTP methods.

---

# 14. `allow_headers`

```python
allow_headers=["*"]
```

This controls which HTTP request headers the frontend is allowed to send.

Using:

```python
allow_headers=["*"]
```

means all headers are allowed.

This is useful when your frontend sends headers such as:

```text
Content-Type
Authorization
Accept
```

For example, JWT authentication commonly uses:

```http
Authorization: Bearer <token>
```

---

# 15. Create the `/home` Endpoint

```python
@app.get("/home")
def home():
    return {
        "message": "CORS enabled"
    }
```

This creates a GET endpoint:

```text
GET /home
```

When someone visits:

```text
http://127.0.0.1:8000/home
```

FastAPI returns:

```json
{
    "message": "CORS enabled"
}
```

---

# 16. Complete Code

The complete code is:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/home")
def home():
    return {
        "message": "CORS enabled"
    }
```

---

# 17. Run the FastAPI Server

Save the file as:

```text
main.py
```

Then run:

```bash
uvicorn main:app --reload
```

Explanation:

```text
uvicorn
```

runs the FastAPI application.

```text
main
```

means `main.py`.

```text
app
```

is the FastAPI object:

```python
app = FastAPI()
```

```text
--reload
```

automatically reloads the server when you modify the code.

---

# 18. Backend URL

After starting the server, FastAPI will normally be available at:

```text
http://127.0.0.1:8000
```

Your endpoint is:

```text
http://127.0.0.1:8000/home
```

Opening it should return:

```json
{
    "message": "CORS enabled"
}
```

---

# 19. FastAPI Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You should see the `/home` endpoint.

You can click:

```text
GET /home
```

and then:

```text
Try it out
```

followed by:

```text
Execute
```

The response will be:

```json
{
    "message": "CORS enabled"
}
```

---

# 20. Calling FastAPI from React

Suppose your React application is running at:

```text
http://localhost:5173
```

You can call the FastAPI endpoint using:

```javascript
fetch("http://127.0.0.1:8000/home")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
```

The response will be:

```javascript
{
    message: "CORS enabled"
}
```

Because:

```python
"http://localhost:5173"
```

was added to:

```python
allow_origins
```

the browser is allowed to make the cross-origin request.

---

# 21. Understanding the Complete Request Flow

Suppose:

```text
React
http://localhost:5173
```

makes a request to:

```text
FastAPI
http://127.0.0.1:8000
```

The flow is:

```text
React Frontend
      |
      | GET /home
      ↓
FastAPI
      |
      ↓
CORSMiddleware
      |
      | Checks Origin
      ↓
http://localhost:5173
      |
      | Allowed
      ↓
/home endpoint
      |
      ↓
JSON Response
```

The browser can then accept the response.

---

# 22. What Happens Without CORS?

If you remove:

```python
app.add_middleware(
    CORSMiddleware,
    ...
)
```

your FastAPI endpoint can still work when accessed directly.

For example:

```text
http://127.0.0.1:8000/home
```

may work in the browser.

However, a frontend running on another origin may receive a browser CORS error when trying to access it.

The important point is:

> CORS is primarily a browser security mechanism. It is not FastAPI refusing to process the HTTP request in the same way as authentication or authorization.

---

# 23. CORS and Same-Origin Policy

Browsers implement the **Same-Origin Policy**.

It prevents a webpage from freely reading resources from another origin.

For example:

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000
```

Different ports mean different origins.

Therefore:

```text
5173 ≠ 8000
```

and the browser considers them cross-origin.

CORS provides a controlled mechanism for allowing such communication.

---

# 24. Development vs Production

During development, you might use:

```python
origins = [
    "http://localhost:5173"
]
```

After deploying your frontend, you should replace or extend it with the real frontend URL.

For example:

```python
origins = [
    "http://localhost:5173",
    "https://myfrontend.example.com"
]
```

This means both your local frontend and deployed frontend can communicate with the API.

---

# 25. Avoid Allowing Every Origin in Production

You may see:

```python
allow_origins=["*"]
```

This means any origin is allowed.

It can be convenient during development, but it is generally better to explicitly list trusted frontend origins in production.

For example:

```python
origins = [
    "https://myfrontend.example.com"
]
```

This is more restrictive and easier to reason about.

---

# 26. Common CORS Error

You may see an error similar to:

```text
Access to fetch at 'http://127.0.0.1:8000/home'
from origin 'http://localhost:5173'
has been blocked by CORS policy
```

This generally means the browser did not receive a CORS response that permits the frontend origin.

Check:

```python
origins = [
    "http://localhost:5173"
]
```

Make sure the origin exactly matches the frontend URL.

---

# 27. `localhost` vs `127.0.0.1`

These should not be treated as identical origins.

For example:

```text
http://localhost:5173
```

and:

```text
http://127.0.0.1:5173
```

are different origins.

If your frontend is running at:

```text
http://127.0.0.1:5173
```

you can allow it explicitly:

```python
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
```

---

# 28. Example with Multiple Frontends

```python
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173"
]
```

Now these three origins are allowed.

---

# 29. Example with Specific HTTP Methods

Instead of:

```python
allow_methods=["*"]
```

you can restrict methods:

```python
allow_methods=[
    "GET",
    "POST",
    "PUT",
    "DELETE"
]
```

This is useful when you want tighter control over your API.

---

# 30. Example with Specific Headers

Instead of:

```python
allow_headers=["*"]
```

you could specify:

```python
allow_headers=[
    "Content-Type",
    "Authorization"
]
```

This is useful when you know exactly which headers your frontend needs.

---

# 31. CORS vs Authentication

CORS is **not authentication**.

CORS answers:

> "Which browser origins are allowed to access my API?"

Authentication answers:

> "Who is this user?"

For example:

```text
CORS
 ↓
Is this frontend origin allowed?

Authentication
 ↓
Who is the user?

Authorization
 ↓
What is the user allowed to do?
```

They solve different problems.

---

# 32. CORS vs Authorization

Consider:

```text
Frontend → FastAPI
```

CORS determines whether the browser permits the frontend to read the response.

Authorization determines whether an authenticated user has permission to perform an operation.

For example:

```text
CORS:
localhost:5173 is allowed.

Authentication:
User successfully logged in.

Authorization:
User is allowed to access /admin.
```

---

# 33. Why `OPTIONS` Requests Matter

Browsers can send an HTTP `OPTIONS` request before certain cross-origin requests.

This is known as a **preflight request**.

For example:

```text
Browser
   |
   | OPTIONS
   ↓
FastAPI
   |
   | Is this request allowed?
   ↓
Browser
   |
   | Actual request
   ↓
FastAPI
```

`CORSMiddleware` handles the CORS preflight behavior for you.

That is one reason middleware is useful.

---

# 34. Important Configuration Summary

| Option              | Purpose                                   |
| ------------------- | ----------------------------------------- |
| `CORSMiddleware`    | Enables CORS handling                     |
| `allow_origins`     | Specifies allowed frontend origins        |
| `allow_credentials` | Allows credentialed cross-origin requests |
| `allow_methods`     | Specifies allowed HTTP methods            |
| `allow_headers`     | Specifies allowed request headers         |

---

# 35. Final Project Structure

A simple project can look like:

```text
fastapi-project/
│
├── main.py
└── requirements.txt
```

`main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/home")
def home():
    return {
        "message": "CORS enabled"
    }
```

Run:

```bash
uvicorn main:app --reload
```

Then:

```text
Backend:
http://127.0.0.1:8000

API:
http://127.0.0.1:8000/home

Swagger:
http://127.0.0.1:8000/docs

Frontend:
http://localhost:5173
```

---

# 36. Quick Revision

Remember the basic pattern:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

In simple words:

```text
allow_origins
    ↓
Which frontend?

allow_credentials
    ↓
Can credentials be included?

allow_methods
    ↓
Which HTTP methods?

allow_headers
    ↓
Which request headers?
```

So the purpose of the entire configuration is:

```text
React/Vite Frontend
http://localhost:5173
          |
          | Cross-Origin Request
          ↓
      CORS Middleware
          |
          ↓
       FastAPI
http://127.0.0.1:8000
```

The middleware allows the trusted frontend to communicate with the FastAPI backend through the browser.
