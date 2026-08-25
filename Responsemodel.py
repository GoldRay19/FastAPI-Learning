from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class User(BaseModel):
    name:str
    age:int
    password:str

class UserResponse(BaseModel):
    name:str
    age:int

@app.get("/user",response_model=UserResponse)
def get_users():
    return{
        "name":"Esha",
        "age":20,
        
    }

@app.get("/user/{id}")
def get_user(get_id:id):
    if(get_id!=1):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )