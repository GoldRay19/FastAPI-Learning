# 🚀 FastAPI Learning

A personal repository for learning and practicing **FastAPI**, a modern, high-performance Python web framework for building APIs.

---

## 📌 About

This repository contains my FastAPI learning journey, including:

* FastAPI basics
* Routing and path parameters
* Query parameters
* Request and response models
* Pydantic validation
* CRUD APIs
* Dependency Injection
* Database integration
* Authentication & Authorization
* File uploads
* Middleware
* Background tasks
* Deployment

---

## 🛠️ Tech Stack

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy
* python-dotenv

---

## 📁 Project Structure

```text
FastApi Learning/
│── .env
│── .gitignore
│── async.py
│── config.py
│── cors.py
│── CREATE.py
│── crud.py
│── data.db
│── delete.py
│── dependencyinjection.py
│── env_cors.py
│── first.py
│── fileupload.py
│── jwt.md
│── jwtauth.py
│── middleware/
│── multiple_routes.py
│── nested_model.py
│── oauth2.py
│── oauth2.md
│── path_parameters.py
│── path_query_body_combo.py
│── query_parameters.py
│── read.py
│── README.md
│── request_body.py
│── Responsemodel.py
│── sql_alchemy.py
│── sqllite.py
│── status_code.py
│── syncasync.py
│── test.db
│── update.py
│── uploads/
│── venv/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd "FastApi Learning"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)

```cmd
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn pydantic sqlalchemy python-dotenv
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

---

## 📝 Sample Code

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

---

## 🎯 Learning Goals

* [ ] Learn FastAPI fundamentals
* [ ] Build REST APIs
* [ ] Perform CRUD operations
* [ ] Use Pydantic models
* [ ] Connect to a database
* [ ] Implement JWT Authentication
* [ ] Handle file uploads
* [ ] Write unit tests
* [ ] Deploy FastAPI applications

---

## 📖 Resources

* FastAPI Official Documentation: https://fastapi.tiangolo.com/
* Python Documentation: https://docs.python.org/3/

---

## 📄 License

This project is created for educational purposes and personal learning.
