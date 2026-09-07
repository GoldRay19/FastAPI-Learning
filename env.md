# Environment Variables and Config File in FastAPI

## 1. What are Environment Variables?

**Environment variables** are values stored outside your application's source code.

They are commonly used for configuration and sensitive information such as:

* Secret keys
* Database URLs
* API keys
* Application settings
* Environment-specific values

For example, instead of writing this directly in Python:

```python
secret_key = "my-secret-key"
```

we can store it in an environment variable:

```text
secret_key=my-secret-key
```

and retrieve it in Python.

---

# 2. Why Use Environment Variables?

Hardcoding configuration directly in the source code is not a good practice.

For example:

```python
secret_key = "my-secret-key"
db_url = "postgresql://user:password@localhost/db"
```

If this code is pushed to GitHub, sensitive information can accidentally become public.

Instead, we can use:

```text
.env
```

to store these values separately.

Then our Python code reads them when the application starts.

---

# 3. What is a `.env` File?

A `.env` file contains environment variables in the following format:

```env
origins=http://localhost:5173
secret_key=my-secret-key
db_url=my-database-url
```

The general structure is:

```text
VARIABLE_NAME=value
```

For example:

```env
SECRET_KEY=abc123
DATABASE_URL=postgresql://localhost/mydb
```

---

# 4. Installing `python-dotenv`

Python does not automatically read `.env` files.

We can use the `python-dotenv` package.

Install it using:

```bash
pip install python-dotenv
```

Or add it to `requirements.txt`:

```text
python-dotenv
```

Then install:

```bash
pip install -r requirements.txt
```

---

# 5. Loading Environment Variables

We can load the `.env` file using:

```python
from dotenv import load_dotenv

load_dotenv()
```

`load_dotenv()` reads the `.env` file and loads its variables into the environment.

For example, suppose `.env` contains:

```env
secret_key=my-secret-key
```

After:

```python
load_dotenv()
```

we can access it using:

```python
os.getenv("secret_key")
```

---

# 6. Using `os.getenv()`

Python's `os` module provides:

```python
os.getenv()
```

to retrieve environment variables.

Example:

```python
import os

secret_key = os.getenv("secret_key")
```

If `.env` contains:

```env
secret_key=my-secret-key
```

then:

```python
secret_key
```

will contain:

```text
my-secret-key
```

---

# 7. Why Create a `config.py` File?

Instead of reading environment variables throughout the application, we can create a separate configuration file.

For example:

```text
project/
│
├── main.py
├── config.py
└── .env
```

The responsibilities are:

```text
.env
 ↓
Stores configuration values

config.py
 ↓
Loads configuration values

main.py
 ↓
Uses configuration values
```

This keeps the application code clean and organized.

---

# 8. `config.py`

A simple `config.py` can be:

```python
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    origins = os.getenv("origins")

    secret_key = os.getenv("secret_key")

    db_url = os.getenv("db_url")


settings = Settings()
```

---

# 9. Understanding the Code

### Import `os`

```python
import os
```

The `os` module allows Python to interact with environment variables.

---

### Import `load_dotenv`

```python
from dotenv import load_dotenv
```

This imports the function used to load variables from `.env`.

---

### Load `.env`

```python
load_dotenv()
```

This loads the environment variables.

---

### Create a Settings Class

```python
class Settings:
```

The class provides one place to keep application configuration.

---

### Read the Origin

```python
origins = os.getenv("origins")
```

This reads the value of:

```env
origins=...
```

from the environment.

---

### Read the Secret Key

```python
secret_key = os.getenv("secret_key")
```

This reads:

```env
secret_key=...
```

---

### Read the Database URL

```python
db_url = os.getenv("db_url")
```

This reads:

```env
db_url=...
```

---

### Create the Settings Object

```python
settings = Settings()
```

Now other files can import the configuration using:

```python
from config import settings
```

and access:

```python
settings.origins
settings.secret_key
settings.db_url
```

---

# 10. Using `config.py` in FastAPI

Suppose `main.py` contains:

```python
from fastapi import FastAPI
from config import settings

app = FastAPI()

print(settings.secret_key)
print(settings.db_url)
```

The application gets its values from:

```text
.env
```

through:

```text
config.py
```

instead of hardcoding them inside `main.py`.

---

# 11. Complete Example

### `.env`

```env
origins=http://localhost:5173
secret_key=my-secret-key
db_url=my-database-url
```

### `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    origins = os.getenv("origins")
    secret_key = os.getenv("secret_key")
    db_url = os.getenv("db_url")


settings = Settings()
```

### `main.py`

```python
from fastapi import FastAPI
from config import settings

app = FastAPI()


@app.get("/config")
def config():
    return {
        "origin": settings.origins
    }
```

The important part is:

```python
from config import settings
```

Then we can access configuration through:

```python
settings.origins
settings.secret_key
settings.db_url
```

---

# 12. `.env` Should Not Be Committed

The `.env` file can contain secrets, so it should normally be added to `.gitignore`.

`.gitignore`:

```gitignore
.env
```

This prevents Git from tracking the `.env` file.

For example:

```text
project/
│
├── main.py
├── config.py
├── .gitignore
└── .env
```

`.gitignore`:

```text
.env
```

---

# 13. Environment Variables in Development and Production

One major advantage of environment variables is that the same code can work in different environments.

For example:

### Development

```env
db_url=localhost_database
```

### Production

```env
db_url=production_database
```

The Python code does not need to change.

It simply reads:

```python
settings.db_url
```

This makes deployment easier.

---

# 14. Default Values

`os.getenv()` can also have a default value.

```python
port = os.getenv("PORT", "8000")
```

If `PORT` exists:

```env
PORT=9000
```

then:

```python
port
```

is:

```text
9000
```

If it doesn't exist, the default is:

```text
8000
```

Another example:

```python
app_name = os.getenv("APP_NAME", "FastAPI App")
```

---

# 15. Environment Variables Are Strings

An important point is that values obtained using:

```python
os.getenv()
```

are strings.

For example:

```env
PORT=8000
```

Then:

```python
port = os.getenv("PORT")
```

gives:

```python
"8000"
```

not:

```python
8000
```

If you need an integer:

```python
port = int(os.getenv("PORT", "8000"))
```

---

# 16. Boolean Environment Variables

Environment variables are also strings for boolean values.

For example:

```env
DEBUG=true
```

This gives:

```python
debug = os.getenv("DEBUG")
```

as:

```text
"true"
```

It is not automatically converted into:

```python
True
```

For larger applications, a settings library such as Pydantic Settings can handle type conversion more cleanly.

---

# 17. Better Configuration Structure

For a growing FastAPI project, you can organize configuration like:

```text
project/
│
├── main.py
│
├── config.py
│
├── .env
│
├── .gitignore
│
└── requirements.txt
```

The flow is:

```text
                 .env
                  │
                  ↓
            Environment Variables
                  │
                  ↓
              config.py
                  │
                  ↓
               settings
                  │
                  ↓
               main.py
                  │
                  ↓
            FastAPI Application
```

---

# 18. Important Security Rule

Do not put sensitive values directly in your Python source code.

Avoid:

```python
secret_key = "123456789"
```

Prefer:

```python
secret_key = os.getenv("secret_key")
```

with:

```env
secret_key=123456789
```

inside `.env`.

And add:

```text
.env
```

to `.gitignore.

---

# 19. Key Concepts to Remember

### Environment Variable

A value stored outside the application source code.

```text
secret_key=my-secret-key
```

### `.env`

A convenient local file for storing environment variables.

```text
.env
```

### `python-dotenv`

A package that loads `.env` variables.

```python
from dotenv import load_dotenv

load_dotenv()
```

### `os.getenv()`

Reads an environment variable.

```python
os.getenv("secret_key")
```

### `config.py`

A separate file used to organize application configuration.

```python
from config import settings
```

### `settings`

A central object through which the application accesses configuration.

```python
settings.secret_key
settings.db_url
settings.origins
```

---

# 20. Final Summary

Instead of:

```python
secret_key = "my-secret-key"
db_url = "my-database-url"
```

inside your FastAPI code, use:

```text
.env
```

```env
secret_key=my-secret-key
db_url=my-database-url
```

Then load them through:

```python
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    secret_key = os.getenv("secret_key")
    db_url = os.getenv("db_url")


settings = Settings()
```

Finally, use them in FastAPI:

```python
from config import settings

print(settings.secret_key)
print(settings.db_url)
```

So the main idea is:

```text
.env
  ↓
load_dotenv()
  ↓
os.getenv()
  ↓
Settings
  ↓
settings
  ↓
FastAPI application
```

This keeps **configuration separate from application code**, makes the project easier to maintain, and helps prevent secrets from being hardcoded into your source code.
