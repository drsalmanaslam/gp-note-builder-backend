from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Pydantic model for validation
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    total: float

router = APIRouter(prefix="/items", tags=["items"])

# In-memory storage
items_db = {}
item_counter = 0

@router.get("/")
def get_items():
    """Get all items"""
    return {"items": list(items_db.values())}

@router.get("/{item_id}")
def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    """Create a new item with validation"""
    global item_counter
    item_counter += 1
    
    # Calculate total with tax
    total = item.price
    if item.tax:
        total += item.tax
    
    new_item = {
        "id": item_counter,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "total": total
    }
    
    items_db[item_counter] = new_item
    return new_item

@router.delete("/{item_id}")
def delete_item(item_id: int):
    """Delete an item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted"}