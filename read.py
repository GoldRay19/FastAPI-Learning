from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base,Session
app=FastAPI()
database_url="sqlite:///./data.db"
engine=create_engine(
    database_url,
    connect_args={"check_same_thread":False}
)
sessionlocal=sessionmaker(bind=engine)
Base=declarative_base()
class Todo(Base):
    __tablename__="todos"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    completed=Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos")
def create_todo(title:str,db:Session=Depends(get_db)):
    todo=Todo(title=title,completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message":"Todo Created",
        "data":todo
    } 

#read all data
@app.get("/todos")
def get_todos(db:Session=Depends(get_db)):
    todo=db.query(Todo).all()
    return {
        "Total":len(todo),
        "Data":todo

    }

#read data based on id
@app.get("/todos/{id}")
def get_todo(id=int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    return todo