import requests 
from fastapi import FastAPI
response=requests.get("https://jsonplaceholder.typicode.com/posts")
data=response.json()
print(data[:2])
app=FastAPI()

@app.get("/posts")
#get all post
def get_posts():
    url="https://jsonplaceholder.typicode.com/posts"
    response=requests.get(url)
    return response.json()

#get a single post
@app.get("/posts/{post_id}")
def get_post(post_id:int):
    url=f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response=requests.get(url)
    return response.json()
