import sqlite3
from fastapi import FastAPI
app=FastAPI()
coon=sqlite3.connect("test.db",check_same_thread=False)
cursor=coon.cursor()

cursor.execute("""
Create Table if not exists todos(
id integer primary key,
title text,
completed text
)
""")
coon.commit()

@app.get("/home")
def get_user():
    return {
        "message":"Sqlite connected"
    }