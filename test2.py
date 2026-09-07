from fastapi import FastAPI
app=FastAPI()
@app.get("/home")
def home():
    return {
        "message":"home route"
    }
@app.get("/add")
def add(a:int,b:int):
    return {
        "result":a+b
    }
