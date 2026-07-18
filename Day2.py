# multiple routes in fastapi
from fastapi import FastAPI
app=FastAPI()

#home route 
@app.get("/")
def home():
    return {"message":"Welcome to home page"}

@app.get("/about")
def about():
    return {"message":"Welcome to the about page"}

@app.get("/leaderboard")
def leaderboard():
    return {"message":"Welcome to the leaderboard page"}