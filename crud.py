from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
todos=[]

class Todo(BaseModel):
    id:int
    title:str
    completed:bool
@app.post("/todo")
def todo(todo:Todo):
    todos.append(todo)
    return {
        "message":"todo created successfully",
        "todo":todo
    }

@app.get("/todo")
def getuser():
    return todos

@app.get("/todo/{id}")
def get_todo(id:int):
    for i in todos:
        if i.id==id:
            return i
    return {
        "error":"todo not found"
    }

@app.put("/todo/{id}")
def update(t_id:int,updates:Todo):
    for i in todos:
        if i.id==t_id:
            i.title=updates.title
            i.completed=updates.completed
            return {
                 "message":"todo successfully updated",
                 "data":i
            }
    return {
        "error":"todo not found"
    }

@app.delete("/todo/{id}")
def delete(id:int):
    for i in todos:
        if i.id==id:
            todos.remove(i)
            return {
                "message":"deleted successfully"
            }
    return {
        "error":"todo not found"
    }