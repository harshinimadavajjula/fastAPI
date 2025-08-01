from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# 1. /hello
@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

# 2. /items/{id}
@app.get("/items/{id}")
def get_item(id: int):
    return {"item_id": id}

# 3. /search?q=value
@app.get("/search")
def search(q: Optional[str] = None):
    return {"search_query": q}

