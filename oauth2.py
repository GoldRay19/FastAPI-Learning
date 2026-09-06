from fastapi import FastAPI,HTTPException,Depends
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext

app=FastAPI()

#jwt config
secret_key="eshajha"
algorithm="HS256"
access_token_expiry_minutes=30

#password hashing setup
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#oauth2 setup
oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

#dummy user db
fake_user_db={
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234")
    }
}

#hash password
def hash_password(password:str):
    return pwd_context.hash(password)


#verify password
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#create token
def create_token(data:dict):
    to_encode=data.copy()
    expiry_date=datetime.now(timezone.utc)+timedelta(minutes=30)
    to_encode.update({
        "exp":expiry_date
    })
    token=jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return token

#login API(oauth2)
@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password"
        )
    access_token=create_token(
        {
            "sub":form_data.username
        }
    )
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }

#token verification
def verify_token(token:str=Depends(oauth2_schema)):
    try:
        payload=jwt.decode(token,secret_key,algorithms=[algorithm])
        username:str=payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return username
    except jwt.JWTError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")


#protected route
@app.get("/secure")
def secure(username:str=Depends(verify_token)):
    return {
        "message":f"secure data accessed to {username}",
        "user":username
    }