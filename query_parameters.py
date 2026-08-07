from fastapi import FastAPI
app=FastAPI()

@app.get("/users")
def users(name: str = None):   #optional query parameters
    return {"name":name}

@app.get("/product")
def product(name: str = None, limit: int = 10, price: int = 0):    #multiple query parameters
    return {"name":name, "limit":limit, "price":price}