# JWT Authentication with FastAPI

## 1. What is Authentication?

**Authentication** means checking whether a user is actually who they claim to be.

For example:

```text
Username: admin
Password: 1234
```

The server verifies these credentials.

If they are correct, the user is authenticated.

---

## 2. What is Authorization?

**Authorization** means checking whether an authenticated user is allowed to access a particular resource.

Example:

```text
Authentication:
"Who are you?"

Authorization:
"Are you allowed to access this?"
```

### Example

```text
Login → Authentication
Access /secure → Authorization
```

---

# 3. What is JWT?

**JWT = JSON Web Token**

JWT is a compact token used to securely transfer information between a client and a server.

After successful login, the server generates a JWT token and sends it to the client.

The client then sends this token when accessing protected routes.

### Basic Flow

```text
User
  ↓
Login
  ↓
Username + Password
  ↓
Server verifies credentials
  ↓
JWT Token Generated
  ↓
Token sent to Client
  ↓
Client sends Token with protected request
  ↓
Server verifies Token
  ↓
Access Granted
```

---

# 4. Structure of JWT

A JWT normally has three parts:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example:

```text
xxxxx.yyyyy.zzzzz
```

## Header

Contains information about the token.

Example:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

`alg` → Algorithm used to sign the token.

`typ` → Type of token.

---

## Payload

Contains information about the user and other claims.

Example:

```json
{
  "sub": "admin",
  "exp": 1780000000
}
```

Common claims:

| Claim | Meaning                   |
| ----- | ------------------------- |
| `sub` | Subject / user identifier |
| `exp` | Expiration time           |
| `iat` | Issued-at time            |
| `iss` | Issuer                    |
| `aud` | Audience                  |

### Important

The JWT payload is **encoded, not encrypted**.

Therefore, sensitive information such as passwords should **never** be stored inside the payload.

---

## Signature

The signature is used to verify that the token has not been modified.

Conceptually:

```text
Signature =
Hash(
    Header + Payload + Secret Key
)
```

The server uses the secret key to verify the signature.

---

# 5. Why Use JWT Authentication?

JWT is useful because:

* It is compact.
* It can be sent with HTTP requests.
* The server can verify the token without storing the token itself in a session.
* It works well with APIs.
* It can contain useful claims such as user ID and expiry time.

---

# 6. Required Libraries

Install FastAPI, Uvicorn and Python-JOSE:

```bash
pip install fastapi uvicorn python-jose
```

`python-jose` provides JWT functionality.

---

# 7. Basic FastAPI JWT Authentication

## Complete Code

```python
from fastapi import FastAPI, HTTPException, Header, Depends
from jose import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI()

secret_key = "eshajha"
algorithm = "HS256"


# Create Token
def create_token(data: dict):

    to_encode = data.copy()

    expiry_date = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({
        "exp": expiry_date
    })

    token = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm
    )

    return token


# Login API - Generate Token
@app.post("/login")
def login(username: str, password: str):

    if username != "admin" or password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_token({
        "sub": username
    })

    return {
        "access_token": token
    }


# Token Verification
def verify_token(token: str = Header(None)):

    try:

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )

        return payload

    except:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# Protected Route
@app.get("/secure")
def secure(user=Depends(verify_token)):

    return {
        "message": "secure data accessed",
        "user": user
    }
```

---

# 8. Understanding the Code

## Step 1: Import Required Modules

```python
from fastapi import FastAPI, HTTPException, Header, Depends
```

### `FastAPI`

Used to create the FastAPI application.

### `HTTPException`

Used to return HTTP errors.

Example:

```python
raise HTTPException(
    status_code=401,
    detail="Invalid credentials"
)
```

### `Header`

Used to read data from HTTP request headers.

### `Depends`

Used for dependency injection.

Here it is used to run token verification before accessing a protected route.

---

```python
from jose import jwt
```

Used to:

* Create JWT tokens.
* Decode JWT tokens.
* Verify JWT tokens.

---

```python
from datetime import datetime, timedelta, timezone
```

Used to calculate token expiration time.

---

# 9. Creating the FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application.

---

# 10. Secret Key and Algorithm

```python
secret_key = "eshajha"
algorithm = "HS256"
```

### Secret Key

The secret key is used to sign and verify JWT tokens.

### Algorithm

`HS256` is the algorithm used for signing the token.

### Important

In a real application, don't hardcode the secret key.

Use an environment variable:

```text
SECRET_KEY=your-secret-key
```

---

# 11. Creating a JWT Token

```python
def create_token(data: dict):
```

This function receives user information and creates a JWT.

Example input:

```python
{
    "sub": "admin"
}
```

---

## Copy the Data

```python
to_encode = data.copy()
```

A copy is created so that the original dictionary is not modified.

---

## Create Expiration Time

```python
expiry_date = datetime.now(timezone.utc) + timedelta(minutes=30)
```

This means:

```text
Current UTC time + 30 minutes
```

So the token will expire after 30 minutes.

---

## Add Expiration to Payload

```python
to_encode.update({
    "exp": expiry_date
})
```

Now the payload contains:

```python
{
    "sub": "admin",
    "exp": expiry_date
}
```

---

## Generate Token

```python
token = jwt.encode(
    to_encode,
    secret_key,
    algorithm=algorithm
)
```

The data is converted into a JWT using:

```text
Payload
   +
Secret Key
   +
Algorithm
   ↓
JWT Token
```

---

## Return Token

```python
return token
```

The generated token is returned.

---

# 12. Login API

```python
@app.post("/login")
def login(username: str, password: str):
```

This creates a POST endpoint:

```text
POST /login
```

The user provides a username and password.

---

## Validate Credentials

```python
if username != "admin" or password != "1234":
```

This checks whether the credentials are correct.

If they are incorrect:

```python
raise HTTPException(
    status_code=401,
    detail="Invalid username or password"
)
```

The server returns:

```text
401 Unauthorized
```

---

# 13. Generate Token After Successful Login

```python
token = create_token({
    "sub": username
})
```

If the login is successful, the `create_token()` function is called.

The payload contains:

```python
{
    "sub": "admin"
}
```

The token is then generated.

---

# 14. Login Response

```python
return {
    "access_token": token
}
```

The client receives the JWT.

Example:

```json
{
    "access_token": "eyJhbGciOiJIUzI1Ni..."
}
```

The client can use this token to access protected routes.

---

# 15. Token Verification

```python
def verify_token(token: str = Header(None)):
```

This function reads the `token` value from the HTTP request header.

Example:

```text
token: eyJhbGciOiJIUzI1Ni...
```

---

## Decode the Token

```python
payload = jwt.decode(
    token,
    secret_key,
    algorithms=[algorithm]
)
```

This verifies and decodes the JWT.

The library checks whether the token is valid and whether its expiration has passed.

If everything is valid, the payload is returned.

Example:

```python
{
    "sub": "admin",
    "exp": 1780000000
}
```

---

# 16. Invalid or Expired Token

```python
except:
    raise HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )
```

If verification fails, the server returns:

```text
401 Unauthorized
```

This can happen when:

* Token is invalid.
* Token was modified.
* Token has expired.
* Token was signed with a different secret key.

---

# 17. Protected Route

```python
@app.get("/secure")
def secure(user=Depends(verify_token)):
```

This creates:

```text
GET /secure
```

The important part is:

```python
Depends(verify_token)
```

It means:

> Before executing `/secure`, FastAPI must execute `verify_token()`.

---

# 18. How `Depends()` Works

Without authentication:

```text
GET /secure
       ↓
secure()
       ↓
Response
```

With authentication:

```text
GET /secure
       ↓
verify_token()
       ↓
Token Valid?
   ↙        ↘
 Yes         No
 ↓            ↓
secure()     401
 ↓
Response
```

So `Depends()` protects the route.

---

# 19. What is `user`?

```python
def secure(user=Depends(verify_token)):
```

`verify_token()` returns the decoded JWT payload.

That returned payload is stored in:

```python
user
```

For example:

```python
user = {
    "sub": "admin",
    "exp": 1780000000
}
```

Therefore:

```python
return {
    "message": "secure data accessed",
    "user": user
}
```

can return the user information.

---

# 20. Testing in Postman

## Step 1: Login

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:8000/login
```

Since `username` and `password` are function parameters, FastAPI treats them as query parameters in this code.

Use:

```text
?username=admin&password=1234
```

So:

```text
POST http://127.0.0.1:8000/login?username=admin&password=1234
```

Response:

```json
{
    "access_token": "your-jwt-token"
}
```

Copy the token.

---

# 21. Access Protected Route

Method:

```text
GET
```

URL:

```text
http://127.0.0.1:8000/secure
```

Go to:

```text
Headers
```

Add:

| Key     | Value            |
| ------- | ---------------- |
| `token` | `your-jwt-token` |

Then send the request.

If the token is valid:

```json
{
    "message": "secure data accessed",
    "user": {
        "sub": "admin",
        "exp": 1780000000
    }
}
```

---

# 22. What Happens if Token is Missing?

If `/secure` is called without the required token:

```text
GET /secure
```

The verification fails and the API returns:

```text
401 Unauthorized
```

---

# 23. What Happens if Token is Expired?

Suppose the token was created at:

```text
10:00 AM
```

and its expiration is:

```text
10:30 AM
```

After 10:30 AM, the token is no longer valid.

The protected route returns:

```text
401 Unauthorized
```

---

# 24. Complete Authentication Flow

```text
                    CLIENT
                       |
                       | POST /login
                       | username + password
                       ↓
                    SERVER
                       |
                       | Verify credentials
                       ↓
                Credentials Correct?
                  /             \
                No               Yes
                ↓                 ↓
              401          create_token()
                                  |
                                  ↓
                              JWT Token
                                  |
                                  ↓
                    Client receives token
                                  |
                                  |
                    GET /secure + token
                                  |
                                  ↓
                         verify_token()
                                  |
                                  ↓
                           jwt.decode()
                                  |
                          Token Valid?
                         /           \
                       No             Yes
                       ↓               ↓
                     401          Payload
                                       |
                                       ↓
                                secure endpoint
                                       |
                                       ↓
                                Protected Data
```

---

# 25. Important Terms to Remember

| Term           | Meaning                               |
| -------------- | ------------------------------------- |
| JWT            | JSON Web Token                        |
| Authentication | Verifying who the user is             |
| Authorization  | Checking what the user can access     |
| Payload        | Data stored inside JWT                |
| `sub`          | Subject/user identifier               |
| `exp`          | Token expiration time                 |
| Secret Key     | Used to sign/verify the JWT           |
| `HS256`        | JWT signing algorithm                 |
| `jwt.encode()` | Creates a JWT                         |
| `jwt.decode()` | Decodes and verifies a JWT            |
| `Header()`     | Reads HTTP request headers            |
| `Depends()`    | Runs a dependency before the endpoint |

---

# 26. Important Security Points

### 1. Never store passwords in JWT

Bad:

```python
{
    "username": "admin",
    "password": "1234"
}
```

Never put passwords inside JWT payloads.

---

### 2. Don't hardcode the secret key

Instead of:

```python
secret_key = "eshajha"
```

use an environment variable in real applications.

---

### 3. Use HTTPS

JWTs should be transmitted over HTTPS in production.

---

### 4. Keep token expiry limited

Don't create tokens that remain valid forever.

For example:

```python
timedelta(minutes=30)
```

creates a limited lifetime.

---

# 27. One-Minute Revision

Remember these four functions/concepts:

```text
create_token()
      ↓
Creates JWT

/login
      ↓
Checks credentials and gives JWT

verify_token()
      ↓
Checks JWT

Depends(verify_token)
      ↓
Protects the route
```

### In one sentence:

**User logs in → server verifies credentials → JWT is generated → client sends JWT with future requests → server verifies JWT → protected route is accessed.**
