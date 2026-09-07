# FastAPI Testing with Pytest

## 1. What is Pytest?

**pytest** is a Python testing framework used to test whether our code is working correctly.

It helps us automatically check:

* Whether a function gives the expected output
* Whether an API returns the correct status code
* Whether an API returns the expected JSON response
* Whether different inputs produce the correct results

Instead of manually opening an API in the browser and checking the response, we can write tests and let pytest check everything automatically.

---

# 2. Installing Pytest

Install pytest using:

```bash
pip install pytest
```

For FastAPI testing, we also use FastAPI's `TestClient`.

```bash
pip install httpx
```

---

# 3. Project Structure

A simple project can look like this:

```text
FastApi Learning/
│
├── test2.py
│
└── test_test2.py
```

Here:

* `test2.py` → contains our FastAPI application
* `test_test2.py` → contains our pytest test cases

---

# 4. FastAPI Application

Our FastAPI application is:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/home")
def home():
    return {
        "message": "home route"
    }


@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }
```

---

# 5. Understanding the FastAPI Code

## Creating the FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()
```

`FastAPI()` creates our FastAPI application.

The application object is stored in the variable:

```python
app
```

---

# 6. `/home` Route

```python
@app.get("/home")
def home():
    return {
        "message": "home route"
    }
```

This creates a GET endpoint:

```text
GET /home
```

When someone sends a request to `/home`, the `home()` function runs.

The response is:

```json
{
    "message": "home route"
}
```

---

# 7. `/add` Route

```python
@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }
```

This endpoint accepts two query parameters:

```text
a
b
```

For example:

```text
/add?a=5&b=8
```

FastAPI converts them to integers because we specified:

```python
a: int
b: int
```

The calculation is:

```python
a + b
```

So:

```text
5 + 8 = 13
```

The response is:

```json
{
    "result": 13
}
```

---

# 8. What is TestClient?

FastAPI provides `TestClient` for testing API endpoints without running the server manually.

We import it using:

```python
from fastapi.testclient import TestClient
```

Then we import our FastAPI application:

```python
from test2 import app
```

Finally, we create the test client:

```python
client = TestClient(app)
```

Now we can send requests to our FastAPI application directly from our tests.

For example:

```python
response = client.get("/home")
```

This behaves like a client sending:

```text
GET /home
```

---

# 9. Writing Our First Test

Our first test is:

```python
def testhome():

    response = client.get("/home")

    assert response.status_code == 200

    assert response.json() == {
        "message": "home route"
    }
```

---

# 10. Test Function Naming

The function is:

```python
def testhome():
```

pytest identifies functions beginning with `test` as test functions.

A more readable convention is:

```python
def test_home():
```

So we can write:

```python
def test_home():
    ...
```

---

# 11. Sending a Request

Inside the test:

```python
response = client.get("/home")
```

We send a GET request to:

```text
/home
```

The response is stored in:

```python
response
```

---

# 12. Checking the Status Code

We use:

```python
assert response.status_code == 200
```

HTTP status code `200` means the request was successful.

So this assertion checks:

```text
Expected: 200
Actual:   response.status_code
```

If both are equal, the test passes.

If they are different, the test fails.

---

# 13. Checking the JSON Response

We use:

```python
response.json()
```

to get the JSON response from the API.

Our API returns:

```json
{
    "message": "home route"
}
```

Therefore, we check:

```python
assert response.json() == {
    "message": "home route"
}
```

This makes sure that the API is returning the exact data we expect.

---

# 14. Testing the `/add` Endpoint

Our second test is:

```python
def testadd():

    response = client.get("/add?a=5&b=8")

    assert response.status_code == 200

    assert response.json() == {
        "result": 13
    }
```

This test sends:

```text
GET /add?a=5&b=8
```

FastAPI receives:

```text
a = 5
b = 8
```

Then the function calculates:

```python
5 + 8
```

which gives:

```text
13
```

The expected response is:

```json
{
    "result": 13
}
```

---

# 15. Complete Test File

Our complete test file can be written as:

```python
from fastapi.testclient import TestClient

from test2 import app


client = TestClient(app)


def test_home():

    response = client.get("/home")

    # Status code check
    assert response.status_code == 200

    # Response data check
    assert response.json() == {
        "message": "home route"
    }


def test_add():

    response = client.get("/add?a=5&b=8")

    # Status code check
    assert response.status_code == 200

    # Response data check
    assert response.json() == {
        "result": 13
    }
```

---

# 16. What is `assert`?

`assert` is used to verify that something is true.

For example:

```python
assert 5 + 5 == 10
```

This passes because:

```text
5 + 5 = 10
```

But:

```python
assert 5 + 5 == 20
```

fails because:

```text
5 + 5 ≠ 20
```

In API testing, we use assertions to compare the actual response with the expected response.

---

# 17. What Happens When We Run pytest?

Suppose our test file is named:

```text
test_test2.py
```

We can run:

```bash
pytest
```

pytest searches for test files and test functions.

It finds:

```python
test_home()
test_add()
```

Then it executes both tests.

---

# 18. Running a Specific Test File

We can run:

```bash
pytest test_test2.py
```

This tells pytest to run the tests inside:

```text
test_test2.py
```

---

# 19. Verbose Output

We can use:

```bash
pytest -v
```

or:

```bash
pytest -v test_test2.py
```

The `-v` means **verbose**.

It gives more detailed information about each test.

Example:

```text
test_test2.py::test_home PASSED
test_test2.py::test_add PASSED

2 passed
```

---

# 20. Understanding PASSED

If pytest displays:

```text
PASSED
```

it means all assertions in that test were successful.

For example:

```python
assert response.status_code == 200
```

and:

```python
assert response.json() == {
    "message": "home route"
}
```

were both correct.

---

# 21. Understanding FAILED

Suppose we accidentally write:

```python
assert response.json() == {
    "message": "hello"
}
```

But our API actually returns:

```json
{
    "message": "home route"
}
```

pytest will report:

```text
FAILED
```

because the actual response does not match the expected response.

---

# 22. Why Test APIs?

Testing is important because applications can become large and complicated.

For example, an API might contain:

```text
/home
/add
/login
/register
/users
/products
/orders
```

Manually checking every endpoint every time we change the code would take a lot of time.

With pytest, we can run:

```bash
pytest
```

and automatically test our endpoints.

---

# 23. Unit Testing vs API Testing

### Unit Testing

Unit testing checks individual pieces of code.

Example:

```python
def add(a, b):
    return a + b
```

We could test:

```python
assert add(5, 8) == 13
```

### API Testing

With FastAPI, we test the endpoint itself:

```python
response = client.get("/add?a=5&b=8")
```

Then check:

```python
assert response.status_code == 200
```

and:

```python
assert response.json() == {
    "result": 13
}
```

---

# 24. Testing Invalid Input

One major advantage of API testing is that we can also test incorrect requests.

For example:

```python
response = client.get("/add?a=hello&b=8")
```

Our endpoint expects:

```python
a: int
```

but receives:

```text
hello
```

FastAPI should return a validation error.

We can test that:

```python
def test_add_invalid_input():

    response = client.get("/add?a=hello&b=8")

    assert response.status_code == 422
```

HTTP `422` means the request could not be processed because the input failed validation.

---

# 25. Testing Missing Parameters

We can also test:

```text
/add?a=5
```

Here `b` is missing.

Test:

```python
def test_add_missing_parameter():

    response = client.get("/add?a=5")

    assert response.status_code == 422
```

FastAPI automatically validates the required parameters.

---

# 26. Final Complete Example

## `test2.py`

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/home")
def home():
    return {
        "message": "home route"
    }


@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }
```

## `test_test2.py`

```python
from fastapi.testclient import TestClient

from test2 import app


client = TestClient(app)


def test_home():

    response = client.get("/home")

    assert response.status_code == 200

    assert response.json() == {
        "message": "home route"
    }


def test_add():

    response = client.get("/add?a=5&b=8")

    assert response.status_code == 200

    assert response.json() == {
        "result": 13
    }


def test_add_invalid_input():

    response = client.get("/add?a=hello&b=8")

    assert response.status_code == 422


def test_add_missing_parameter():

    response = client.get("/add?a=5")

    assert response.status_code == 422
```

---

# 27. Important Commands

Install pytest:

```bash
pip install pytest
```

Install the HTTP client dependency:

```bash
pip install httpx
```

Run all tests:

```bash
pytest
```

Run a particular file:

```bash
pytest test_test2.py
```

Run with detailed output:

```bash
pytest -v
```

Run a specific test:

```bash
pytest test_test2.py::test_home
```

---

# 28. Key Concepts to Remember

| Concept                | Meaning                                |
| ---------------------- | -------------------------------------- |
| `pytest`               | Python testing framework               |
| `TestClient`           | Sends requests to FastAPI during tests |
| `client.get()`         | Sends a GET request                    |
| `response`             | Stores the API response                |
| `response.status_code` | Gets HTTP status code                  |
| `response.json()`      | Gets JSON response                     |
| `assert`               | Checks expected vs actual result       |
| `200`                  | Successful request                     |
| `422`                  | Validation error                       |
| `PASSED`               | Test succeeded                         |
| `FAILED`               | Test did not meet the expected result  |

---

# Conclusion

**pytest** allows us to automatically test our FastAPI application.

The basic testing flow is:

```text
Write API
   ↓
Create TestClient
   ↓
Send request
   ↓
Receive response
   ↓
Check status code
   ↓
Check response data
   ↓
pytest → PASSED / FAILED
```

For our application:

```python
response = client.get("/home")
```

tests the `/home` endpoint, while:

```python
response = client.get("/add?a=5&b=8")
```

tests the `/add` endpoint.

We then use `assert` to make sure that the API behaves exactly as expected.

**In short:**

> Pytest + FastAPI TestClient = automated API testing.
