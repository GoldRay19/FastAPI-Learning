from fastapi import FastAPI,status,HTTPException
app=FastAPI()
@app.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message":"user created successfully"
    }

@app.get("/user")
def get_users():
    return {
        "statu_code":status.HTTP_200_OK,
        "status":"Success",
        "message":"received successfully",
        "data":{
            "name":"esha",
            "age":20
        }
    }

@app.get("/user/{id}")
def get_user(id:int):
    if(id!=1):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "name":"esha",
        "age":20
    }