from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class Address(BaseModel):
    stree:str
    pincode:int
    area:str
    country:str
    
class User(BaseModel):
    name:str
    age:int
    email:str
    address:Address
    
@app.post("/user")
def users(user:User):
    return{
        "message":"user created successfully",
        "data":user
    }