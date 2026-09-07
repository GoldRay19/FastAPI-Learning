from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
app= FastAPI()

origins=settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/home")
def home():
    return {
        "message":"CORS enabled"
    }