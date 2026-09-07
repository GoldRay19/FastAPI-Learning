import os
from dotenv import load_dotenv
load_dotenv()
class Settings():
    origins=os.getenv("origins")
    secret_key=os.getenv("secret_key")
    db_url=os.getenv("db_url")

settings=Settings()