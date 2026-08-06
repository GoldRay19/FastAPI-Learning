from fastapi import FastAPI
app=FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to home page"}

@app.get("/users/{user_id}")
def user(user_id:int):
    return {"message":"welcome to the user page","user_id": user_id}

