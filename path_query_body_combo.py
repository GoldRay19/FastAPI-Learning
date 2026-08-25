from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: str


@app.post("/user")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "data": user
    }


@app.get("/user/{id}")
def get_user(id: int):
    return {
        "message": "User retrieved successfully",
        "id": id
    }


@app.put("/user/{id}")
def update_user(id: int, user: User):
    return {
        "message": "User updated successfully",
        "id": id,
        "data": user
    }