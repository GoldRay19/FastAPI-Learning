from fastapi.testclient import TestClient
from test2 import app
client=TestClient(app)

def testhome():
    response=client.get("/home")
    #status code check
    assert response.status_code==200
    #response data check
    assert response.json()=={
        "message":"home route"
    }

def testadd():
    response=client.get("/add?a=5&b=8")
    assert response.status_code==200
    assert response.json()=={
        "result":13
    }

    