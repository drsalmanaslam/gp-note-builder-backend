from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def get_products():
    """Get all products"""
    return {"products": ["Laptop", "Phone", "Tablet", "Headphones"]}

@router.get("/{product_id}")
def get_product(product_id: int):
    """Get a specific product by ID"""
    return {
        "product_id": product_id,
        "name": f"Product {product_id}",
        "price": 99.99
    }

@router.post("/")
def create_product(name: str, price: float):
    """Create a new product"""
    return {
        "message": f"Product {name} created!",
        "product": {"name": name, "price": price}
    }