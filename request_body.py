from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()

@app.post("/user")
def user(name:str):
    return {"name":name}

#real world use
class User(BaseModel): 
    name: str
    age:int
    email:str
@app.post("/leaderboard")
def leaderborad(user:User):
    return {
        "data":user,
        "message":"user created successfully"
    }