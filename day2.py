from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Create FastAPI app instance
app = FastAPI()

# Route 1: Basic root route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Route 2: Path parameter example
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": "You requested item"}

# Route 3: Query parameter example
@app.get("/search/")
def search_item(q: Optional[str] = None):
    return {"query": q}

# Route 4: Request body model
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

@app.post("/products/")
def create_product(product: Product):
    return {
        "message": "Product created successfully!",
        "product": product
    }
