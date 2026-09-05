from fastapi import FastAPI,HTTPException,status,Header,Depends

app=FastAPI()
def verify_token(token:str=Header(None)):
    if(token!="mysecret"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not authorized"
        )
    return {
        "message":"user authorized"
    }
    
@app.getv("/user")
def User(user=Depends(verify_token)):
    return user