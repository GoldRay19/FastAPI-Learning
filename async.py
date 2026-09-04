import time
import asyncio
from fastapi import FastAPI
app=FastAPI()
@app.get("/home")
async def home():
    await asyncio.sleep(3)
    return {
        "messge":"Async API"
    }