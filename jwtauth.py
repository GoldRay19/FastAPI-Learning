from fastapi import FastAPI,HTTPException,Header,Depends
from jose import jwt
from datetime import datetime,timedelta,timezone

app=FastAPI()

secret_key="eshajha"
algorithm="HS256"

#create token
def create_token(data:dict):
    to_encode=data.copy()
    expiry_date=datetime.now(timezone.utc)+timedelta(minutes=30)
    to_encode.update({
        "exp":expiry_date
    })
    token=jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return token

#login API(Token Generate)
@app.post("/login")
def login(username:str,password:str):
    if username!="admin" or password!="1234":
        raise HTTPException(status_code=401,detail="Invalid username or password")
    token=create_token({
        "sub":username
    })
    return {
        "access_token":token
    }


#token verification
def verify_token(token:str=Header(None)):
    try:
        payload=jwt.decode(token,secret_key,algorithms=[algorithm])
        return payload
    except:
        raise HTTPException(status_code=401,detail="Invalid or expired token")


#protected route
@app.get("/secure")
def secure(user=Depends(verify_token)):
    return {
        "message":"secure data accessed",
        "user":user
    }