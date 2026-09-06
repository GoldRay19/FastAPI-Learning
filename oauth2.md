# FastAPI JWT Authentication — Complete Explainable Guide

This document explains a complete JWT-based authentication system built using **FastAPI**.

The implementation includes:

* User login
* Password hashing with bcrypt
* Password verification
* JWT token creation
* JWT token expiration
* OAuth2 password flow
* OAuth2 Bearer token handling
* Token verification
* Protected routes
* FastAPI Dependency Injection
* Postman testing
* Common errors and fixes

---

# 1. Complete Code

```python
from fastapi import FastAPI, HTTPException, Depends

from jose import jwt, JWTError

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext


app = FastAPI()


# JWT config

secret_key = "eshajha"

algorithm = "HS256"

access_token_expiry_minutes = 30


# Password hashing setup

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# OAuth2 setup

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="login"
)


# Dummy user database

fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("1234")
    }
}


# Hash password

def hash_password(password: str):
    return pwd_context.hash(password)


# Verify password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# Create JWT token

def create_token(data: dict):

    to_encode = data.copy()

    expiry_date = (
        datetime.now(timezone.utc)
        + timedelta(minutes=30)
    )

    to_encode.update({
        "exp": expiry_date
    })

    token = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm
    )

    return token


# Login API

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = fake_user_db.get(form_data.username)

    if not user or not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password"
        )

    access_token = create_token(
        {
            "sub": form_data.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Token verification

def verify_token(
    token: str = Depends(oauth2_schema)
):

    try:

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )

        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# Protected route

@app.get("/secure")
def secure(
    username: str = Depends(verify_token)
):

    return {
        "message": f"secure data accessed to {username}",
        "user": username
    }
```

---

# 2. What Are We Building?

We are building an authentication system using:

```text
FastAPI
   |
   ├── Username + Password
   |
   ├── Password Hashing
   |
   ├── Login
   |
   ├── JWT Token Generation
   |
   ├── JWT Token Verification
   |
   └── Protected API
```

The complete flow is:

```text
User
 |
 | username + password
 v
POST /login
 |
 v
Check user
 |
 v
Verify hashed password
 |
 v
Create JWT
 |
 v
Return access_token
 |
 v
Client stores token
 |
 | Authorization: Bearer <token>
 v
GET /secure
 |
 v
Verify JWT
 |
 v
Extract username
 |
 v
Allow access
```

---

# 3. Authentication vs Authorization

## Authentication

Authentication answers:

> "Who are you?"

Example:

```text
Username: admin
Password: 1234
```

The server checks whether these credentials are correct.

If correct:

```text
User is authenticated
```

---

## Authorization

Authorization answers:

> "What are you allowed to access?"

For example:

```text
Normal user → /profile
Admin       → /admin
```

A user may be authenticated but still not have permission to access every resource.

---

# 4. Why Password Hashing Is Required

We should NEVER store passwords directly like this:

```python
"password": "1234"
```

If the database gets leaked, the actual passwords would be exposed.

Instead, we store:

```text
1234
 |
 | bcrypt
 v
$2b$12$................................
```

The stored value is called a:

```text
hashed password
```

---

# 5. Cryptographic Hashing

A hash function converts data into another value.

Conceptually:

```text
password
   |
   v
hash function
   |
   v
hashed value
```

For example:

```text
1234
 ↓
bcrypt
 ↓
$2b$12$....
```

We do not normally reverse the hash to get the password.

During login, we instead compare:

```text
Entered password
       |
       v
verify against
       |
       v
Stored hash
```

---

# 6. Passlib and CryptContext

This line creates our password hashing configuration:

```python
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
```

`CryptContext` provides functions for password hashing and verification.

We are telling Passlib:

```text
Use bcrypt for password hashing.
```

---

# 7. Creating the Dummy User Database

Our example uses:

```python
fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("1234")
    }
}
```

This is NOT a real database.

It is only for learning.

The structure is:

```text
fake_user_db
     |
     └── admin
          |
          ├── username
          |
          └── hashed_password
```

The password:

```text
1234
```

is hashed before being stored.

Therefore the server does not store:

```text
1234
```

directly.

---

# 8. Hash Password Function

```python
def hash_password(password: str):
    return pwd_context.hash(password)
```

This function accepts a normal password:

```python
hash_password("1234")
```

and returns a bcrypt hash.

Example:

```text
1234
 ↓
bcrypt
 ↓
$2b$12$....
```

---

# 9. Verify Password Function

```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
```

This function checks whether a plain password matches the stored hash.

Example:

```python
verify_password(
    "1234",
    stored_hash
)
```

Result:

```text
True
```

If the password is wrong:

```text
False
```

---

# 10. Important Difference Between Hashing and Verification

When creating a user:

```text
Password
   ↓
hash()
   ↓
Store hash
```

During login:

```text
Entered password
   ↓
verify()
   ↓
Compare with stored hash
```

We should NOT do:

```python
pwd_context.hash(password) == stored_hash
```

because bcrypt uses a salt, so hashing the same password again can produce a different hash.

Use:

```python
pwd_context.verify(
    plain_password,
    hashed_password
)
```

instead.

---

# 11. JWT

JWT stands for:

```text
JSON Web Token
```

A JWT is commonly used to represent authenticated user information.

A JWT looks conceptually like:

```text
xxxxx.yyyyy.zzzzz
```

It has three parts:

```text
Header.Payload.Signature
```

---

# 12. JWT Header

The header contains information such as the algorithm.

For example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

---

# 13. JWT Payload

The payload contains claims.

Our application uses:

```python
{
    "sub": "admin",
    "exp": expiry_date
}
```

Here:

```text
sub
```

means the subject of the token.

We use it to store the username.

So:

```text
sub = admin
```

means:

```text
This token belongs to admin.
```

---

# 14. JWT Expiration

We add:

```python
"exp": expiry_date
```

`exp` means:

```text
Expiration Time
```

After the token expires, it should no longer be accepted.

Our code creates an expiration time 30 minutes into the future.

---

# 15. JWT Configuration

```python
secret_key = "eshajha"

algorithm = "HS256"

access_token_expiry_minutes = 30
```

## secret_key

The secret key is used to sign and verify the JWT.

```text
JWT
 |
 | secret key
 v
Signature
```

The same secret key is used later to verify the token.

---

## algorithm

```python
algorithm = "HS256"
```

This tells JWT to use the HS256 signing algorithm.

---

## Expiration

```python
access_token_expiry_minutes = 30
```

The intention is that the access token should remain valid for 30 minutes.

A cleaner implementation would use this variable inside `create_token()` rather than hard-coding `30`.

---

# 16. Creating the JWT Token

Our function:

```python
def create_token(data: dict):
```

accepts data that we want to put into the token.

For example:

```python
{
    "sub": "admin"
}
```

---

# 17. Why Do We Copy the Data?

```python
to_encode = data.copy()
```

We make a copy so that adding the expiration claim does not modify the original dictionary.

Original:

```python
data = {
    "sub": "admin"
}
```

Copy:

```python
to_encode = {
    "sub": "admin"
}
```

Then we add:

```python
"exp": expiry_date
```

---

# 18. Creating the Expiration Date

```python
expiry_date = (
    datetime.now(timezone.utc)
    + timedelta(minutes=30)
)
```

First:

```python
datetime.now(timezone.utc)
```

gets the current UTC time.

Then:

```python
timedelta(minutes=30)
```

represents 30 minutes.

Adding them gives:

```text
Current UTC time
       +
    30 minutes
       =
Expiration time
```

---

# 19. Adding Expiration to Payload

```python
to_encode.update({
    "exp": expiry_date
})
```

Now the payload becomes conceptually:

```python
{
    "sub": "admin",
    "exp": "future time"
}
```

---

# 20. Encoding the JWT

```python
token = jwt.encode(
    to_encode,
    secret_key,
    algorithm=algorithm
)
```

This creates the JWT.

Inputs:

```text
Payload
Secret Key
Algorithm
```

Output:

```text
JWT access token
```

---

# 21. Returning the Token

```python
return token
```

The generated JWT is returned to the login function.

---

# 22. OAuth2

OAuth2 is an authorization framework.

FastAPI provides security utilities that make implementing common OAuth2 flows easier.

Our code uses:

```python
OAuth2PasswordBearer
```

and:

```python
OAuth2PasswordRequestForm
```

These two are important but serve different purposes.

---

# 23. OAuth2PasswordBearer

```python
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

This tells FastAPI that the application uses a Bearer token.

The token is expected in the HTTP header:

```http
Authorization: Bearer <token>
```

---

# 24. What Does `tokenUrl="login"` Mean?

```python
tokenUrl="login"
```

means the OAuth2 token endpoint is:

```text
POST /login
```

It does NOT automatically create the login endpoint.

We still create:

```python
@app.post("/login")
```

ourselves.

---

# 25. OAuth2PasswordRequestForm

Our login endpoint contains:

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

This means FastAPI expects OAuth2-style form data.

The client sends:

```text
username=admin
password=1234
```

The framework gives us:

```python
form_data.username
form_data.password
```

---

# 26. Why `Depends()`?

FastAPI has a powerful feature called:

```text
Dependency Injection
```

When we write:

```python
Depends()
```

we are telling FastAPI:

> "Get this value/dependency for me."

For:

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

FastAPI creates the form object and passes it to the function.

---

# 27. Login Endpoint

```python
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
```

This creates:

```text
POST /login
```

The user sends username and password.

---

# 28. Finding the User

```python
user = fake_user_db.get(form_data.username)
```

Suppose the user sends:

```text
username = admin
```

Then:

```python
fake_user_db.get("admin")
```

returns:

```python
{
    "username": "admin",
    "hashed_password": "..."
}
```

---

# 29. Checking Credentials

```python
if not user or not verify_password(
    form_data.password,
    user["hashed_password"]
):
```

There are two checks.

## Check 1 — Does user exist?

```python
not user
```

If the username doesn't exist:

```text
True
```

and login fails.

---

## Check 2 — Is password correct?

```python
verify_password(
    form_data.password,
    user["hashed_password"]
)
```

If correct:

```text
True
```

If incorrect:

```text
False
```

---

# 30. Why `or` Is Used?

```python
if not user or not verify_password(...):
```

This means:

```text
If user doesn't exist
OR
password doesn't match
```

then reject the login.

---

# 31. Invalid Login

If authentication fails:

```python
raise HTTPException(
    status_code=400,
    detail="Invalid username or password"
)
```

The API returns an error.

Conceptually:

```json
{
    "detail": "Invalid username or password"
}
```

---

# 32. Creating Access Token After Successful Login

If the username and password are correct:

```python
access_token = create_token(
    {
        "sub": form_data.username
    }
)
```

For:

```text
admin
```

the payload becomes:

```python
{
    "sub": "admin"
}
```

Then `create_token()` adds the expiration time.

---

# 33. Login Response

The API returns:

```python
return {
    "access_token": access_token,
    "token_type": "bearer"
}
```

Example:

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

The client can now use this token to access protected APIs.

---

# 34. What Is Bearer Authentication?

Bearer means:

> Whoever possesses this valid token can present it as proof of authentication.

The client sends:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

The server reads the token and verifies it.

---

# 35. Token Verification

We create:

```python
def verify_token(
    token: str = Depends(oauth2_schema)
):
```

This function is responsible for verifying the token.

---

# 36. How Does `oauth2_schema` Get the Token?

Because:

```python
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

FastAPI looks for:

```http
Authorization: Bearer <token>
```

The actual JWT is extracted from the header.

Then it is passed into:

```python
token
```

inside:

```python
verify_token()
```

---

# 37. Decoding the JWT

```python
payload = jwt.decode(
    token,
    secret_key,
    algorithms=[algorithm]
)
```

The server verifies the token using:

```text
Token
Secret Key
Algorithm
```

If everything is valid, the payload is returned.

For example:

```python
{
    "sub": "admin",
    "exp": ...
}
```

---

# 38. What Does Decode Actually Check?

JWT decoding/verification checks important things such as:

* Signature
* Token structure
* Algorithm
* Expiration claim when applicable

If the token has expired or the signature is invalid, an exception is raised.

---

# 39. Extracting Username

```python
username: str = payload.get("sub")
```

We stored:

```python
"sub": "admin"
```

while creating the token.

Now we retrieve it:

```python
payload.get("sub")
```

Result:

```text
admin
```

---

# 40. What If `sub` Is Missing?

```python
if username is None:
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
```

A token may technically be decodable but still not contain the claim our application requires.

Therefore we reject it.

---

# 41. Handling Invalid or Expired Tokens

```python
except JWTError:
    raise HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )
```

If JWT verification fails, the user receives:

```text
401 Unauthorized
```

---

# 42. Why Status Code 401?

`401 Unauthorized` is used when the request does not contain valid authentication credentials.

Examples:

```text
No token
Invalid token
Expired token
Invalid credentials
```

---

# 43. Protected Route

Now we have:

```python
@app.get("/secure")
def secure(
    username: str = Depends(verify_token)
):
```

This is a protected endpoint.

The important part is:

```python
Depends(verify_token)
```

---

# 44. How the Protected Route Works

When the user requests:

```http
GET /secure
```

FastAPI first executes:

```python
verify_token()
```

Only if verification succeeds does FastAPI execute:

```python
secure()
```

Flow:

```text
GET /secure
     |
     v
verify_token()
     |
     ├── Invalid → 401
     |
     └── Valid
          |
          v
     secure()
```

---

# 45. Dependency Injection Chain

There is actually a dependency chain:

```text
secure()
   |
   | Depends(verify_token)
   v
verify_token()
   |
   | Depends(oauth2_schema)
   v
OAuth2PasswordBearer
   |
   v
Extract Bearer token
```

Then:

```text
Token
 ↓
JWT decode
 ↓
Extract sub
 ↓
Return username
 ↓
secure(username)
```

---

# 46. Why Does `username` Get a Value?

This:

```python
username: str = Depends(verify_token)
```

means:

```text
Run verify_token()
```

Suppose `verify_token()` returns:

```python
"admin"
```

FastAPI effectively provides:

```python
username = "admin"
```

to the route.

So the response becomes:

```json
{
    "message": "secure data accessed to admin",
    "user": "admin"
}
```

---

# 47. Complete Authentication Flow

The entire application works like this:

```text
                 LOGIN
                   |
                   v
        POST /login
                   |
                   v
       Username + Password
                   |
                   v
          Find user in DB
                   |
                   v
        Verify bcrypt hash
             /         \
           No           Yes
           |             |
           v             v
         400        Create JWT
                         |
                         v
                   Return Token
                         |
                         v
              Client stores token
                         |
                         |
                         v
                 GET /secure
                         |
                         v
             Authorization Header
                         |
                         v
                 Bearer <JWT>
                         |
                         v
               Extract JWT
                         |
                         v
                  Decode JWT
                    /      \
                 Invalid    Valid
                   |          |
                   v          v
                  401     Extract sub
                              |
                              v
                           username
                              |
                              v
                       Protected Route
                              |
                              v
                         Return Data
```

---

# 48. Postman Testing

## Step 1 — Start FastAPI

Run:

```bash
uvicorn main:app --reload
```

If your file is named:

```text
main.py
```

then:

```bash
uvicorn main:app --reload
```

---

# 49. Step 2 — Login

Create a Postman request:

```text
POST http://127.0.0.1:8000/login
```

Go to:

```text
Body
  ↓
x-www-form-urlencoded
```

Add:

```text
username    admin
password    1234
```

Do NOT send this as JSON.

Correct:

```text
x-www-form-urlencoded
```

Not:

```text
raw → JSON
```

---

# 50. Login Response

You should receive:

```json
{
    "access_token": "YOUR_JWT_TOKEN",
    "token_type": "bearer"
}
```

Copy the:

```text
access_token
```

---

# 51. Step 3 — Access Protected Route

Create:

```text
GET http://127.0.0.1:8000/secure
```

Go to:

```text
Authorization
```

Select:

```text
Bearer Token
```

Paste your JWT into:

```text
Token
```

Then send the request.

---

# 52. Successful Response

You should get something similar to:

```json
{
    "message": "secure data accessed to admin",
    "user": "admin"
}
```

This proves:

```text
Login successful
       ↓
JWT generated
       ↓
JWT sent
       ↓
JWT verified
       ↓
Protected route accessed
```

---

# 53. What Happens If You Don't Send a Token?

Request:

```http
GET /secure
```

without:

```http
Authorization: Bearer <token>
```

FastAPI's OAuth2 security dependency will reject the request.

The endpoint cannot be accessed without authentication.

---

# 54. What Happens If the Token Is Wrong?

Suppose you send:

```text
Bearer abc123
```

JWT decoding will fail.

Result:

```text
401 Unauthorized
```

with:

```json
{
    "detail": "Invalid or expired token"
}
```

---

# 55. What Happens If the Token Expires?

Our token contains:

```python
"exp": expiry_date
```

After the expiration time passes, JWT validation fails.

Result:

```text
401 Unauthorized
```

---

# 56. Why JWT Is Useful

Without JWT, the server might need to maintain session state.

With JWT:

```text
Login
  ↓
JWT
  ↓
Client sends JWT with future requests
  ↓
Server verifies JWT
```

The token carries the necessary claims.

---

# 57. JWT Does NOT Mean the Password Is Inside the Token

Our JWT contains:

```python
{
    "sub": "admin",
    "exp": ...
}
```

It does NOT contain:

```text
password = 1234
```

The password is verified during login.

After successful authentication, the JWT represents the authenticated session/access.

---

# 58. JWT Is Signed, Not Necessarily Encrypted

This is an important concept.

JWT payload data should not be treated as secret merely because it is encoded.

JWT commonly provides:

```text
Integrity / authenticity
```

through its signature.

It does not automatically provide:

```text
Confidentiality
```

Therefore sensitive information such as passwords should never be put into the JWT payload.

Good:

```python
{
    "sub": "admin"
}
```

Bad:

```python
{
    "username": "admin",
    "password": "1234"
}
```

---

# 59. Why `sub` Is Used?

JWT defines standard registered claims.

One common claim is:

```text
sub
```

which represents the subject.

We use:

```python
"sub": form_data.username
```

So the token identifies the user.

---

# 60. Authentication Flow in Simple Words

Imagine an office.

## Step 1 — Login

You tell the receptionist:

```text
Username: admin
Password: 1234
```

The receptionist checks your credentials.

---

## Step 2 — Token

If correct, the receptionist gives you an access card.

```text
JWT token
```

---

## Step 3 — Protected Resource

You want to enter a restricted room.

You show your access card:

```text
Authorization: Bearer <JWT>
```

---

## Step 4 — Verification

Security checks whether the card:

```text
is valid
is authentic
is not expired
```

---

## Step 5 — Access

If everything is valid:

```text
Access granted
```

This is similar to our `/secure` endpoint.

---

# 61. Important Security Improvements

The example is designed for learning.

For production, several things should be improved.

---

## 61.1 Don't Hard-Code the Secret Key

Current:

```python
secret_key = "eshajha"
```

Production should use an environment variable.

Conceptually:

```text
Environment Variable
        |
        v
SECRET_KEY
```

The secret should not be committed to GitHub.

---

# 62. 61.2 Don't Use a Fake Database

Current:

```python
fake_user_db = {...}
```

Real applications use databases such as:

```text
PostgreSQL
MySQL
SQLite
MongoDB
```

The user record would contain something like:

```text
id
username
email
hashed_password
```

---

# 63. 61.3 Don't Generate the Hash Every Time the Application Starts

The example has:

```python
"hashed_password": pwd_context.hash("1234")
```

This is acceptable for a simple demonstration.

In a real application, the password would be hashed when the user registers and the resulting hash would be stored in the database.

Then during login:

```text
Entered password
       ↓
verify()
       ↓
Stored hash
```

---

# 64. 61.4 Use the Expiry Variable

We declared:

```python
access_token_expiry_minutes = 30
```

but then used:

```python
timedelta(minutes=30)
```

A cleaner implementation is:

```python
timedelta(
    minutes=access_token_expiry_minutes
)
```

Then changing:

```python
access_token_expiry_minutes = 60
```

automatically changes the token lifetime.

---

# 65. 61.5 Use Strong Secrets

A secret such as:

```text
eshajha
```

is not suitable for production.

Use a long, randomly generated secret.

---

# 66. 61.6 HTTPS Is Important

JWTs are credentials.

Therefore they should be transmitted over:

```text
HTTPS
```

rather than plain HTTP in production.

---

# 67. Important Installation Requirements

Typical packages for this example include:

```bash
pip install fastapi uvicorn python-jose passlib[bcrypt] python-multipart
```

Then run:

```bash
uvicorn main:app --reload
```

---

# 68. Why `python-multipart`?

`OAuth2PasswordRequestForm` reads form data.

FastAPI requires multipart/form parsing support for form handling.

If it is missing, you may see an error telling you to install:

```text
python-multipart
```

Install it with:

```bash
pip install python-multipart
```

---

# 69. Important Correction in Exception Handling

Because we imported:

```python
from jose import jwt, JWTError
```

the clean exception handling is:

```python
except JWTError:
```

rather than:

```python
except jwt.JWTError:
```

So use:

```python
try:
    payload = jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm]
    )

except JWTError:
    raise HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )
```

---

# 70. Difference Between `OAuth2PasswordBearer` and `OAuth2PasswordRequestForm`

This is one of the most important things to remember.

## OAuth2PasswordRequestForm

Used during:

```text
LOGIN
```

It reads:

```text
username
password
```

Example:

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

---

## OAuth2PasswordBearer

Used for:

```text
PROTECTED ROUTES
```

It extracts the Bearer token from:

```http
Authorization: Bearer <token>
```

Example:

```python
token: str = Depends(oauth2_schema)
```

---

# 71. Easy Way to Remember

```text
OAuth2PasswordRequestForm
            ↓
          LOGIN
            ↓
     username + password
```

and:

```text
OAuth2PasswordBearer
            ↓
     PROTECTED ROUTE
            ↓
       Bearer token
```

---

# 72. Difference Between `jwt.encode()` and `jwt.decode()`

## Encode

```python
jwt.encode(...)
```

means:

```text
Payload → JWT
```

Used during login.

---

## Decode

```python
jwt.decode(...)
```

means:

```text
JWT → Verified Payload
```

Used when accessing protected routes.

---

# 73. Difference Between `hash()` and `verify()`

## Hash

```python
pwd_context.hash(password)
```

Used when storing a password.

```text
Password → Hash
```

---

## Verify

```python
pwd_context.verify(
    plain_password,
    hashed_password
)
```

Used during login.

```text
Password + Stored Hash → True/False
```

---

# 74. Complete Concept Map

```text
                    FASTAPI
                       |
          +------------+------------+
          |                         |
     Authentication           Protected APIs
          |                         |
          v                         v
      /login                     /secure
          |                         |
          v                         |
 Username + Password                |
          |                         |
          v                         |
    bcrypt verify                   |
          |                         |
          v                         |
      JWT encode                    |
          |                         |
          v                         |
    Access Token -------------------+
                                    |
                                    v
                         OAuth2PasswordBearer
                                    |
                                    v
                              Extract token
                                    |
                                    v
                              jwt.decode()
                                    |
                         +----------+----------+
                         |                     |
                      Invalid                 Valid
                         |                     |
                         v                     v
                       401              Extract `sub`
                                               |
                                               v
                                           username
                                               |
                                               v
                                        Access granted
```

---

# 75. The Most Important Lines to Understand

If you are learning this code for FastAPI/backend development, focus especially on these lines.

### Password hashing

```python
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
```

### Password verification

```python
pwd_context.verify(
    plain_password,
    hashed_password
)
```

### JWT configuration

```python
secret_key = "..."
algorithm = "HS256"
```

### JWT creation

```python
jwt.encode(
    payload,
    secret_key,
    algorithm=algorithm
)
```

### OAuth2 bearer extraction

```python
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

### Token extraction

```python
token: str = Depends(oauth2_schema)
```

### JWT verification

```python
jwt.decode(
    token,
    secret_key,
    algorithms=[algorithm]
)
```

### Protected endpoint

```python
username: str = Depends(verify_token)
```

---

