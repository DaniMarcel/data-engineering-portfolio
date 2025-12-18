"""FastAPI Backend - E-commerce REST API"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

# ============= MODELS =============

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float
    stock: int

class Customer(BaseModel):
    customer_id: int
    name: str
    email: str
    created_at: datetime

class Order(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    total: float
    status: str = "pending"
    created_at: datetime

# ============= DATABASE SIMULATION =============

class Database:
    """Simple in-memory database"""
    
    def __init__(self):
        self.products = self._load_products()
        self.customers = []
        self.orders = []
    
    def _load_products(self):
        """Load initial products"""
        return {
            1: Product(product_id=1, name="Laptop Pro", category="Electronics", price=1299.99, stock=15),
            2: Product(product_id=2, name="Wireless Mouse", category="Accessories", price=29.99, stock=100),
            3: Product(product_id=3, name="Mechanical Keyboard", category="Accessories", price=89.99, stock=50),
            4: Product(product_id=4, name="27\" Monitor", category="Electronics", price=399.99, stock=20),
            5: Product(product_id=5, name="USB-C Hub", category="Accessories", price=49.99, stock=75),
        }

db = Database()

# ============= API =============

app = FastAPI(
    title="E-commerce API",
    description="REST API for e-commerce platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= ROUTES =============

@app.get("/")
def root():
    """API root"""
    return {
        "message": "E-commerce API v1.0",
        "endpoints": {
            "products": "/products",
            "customers": "/customers",
            "orders": "/orders",
            "analytics": "/analytics"
        }
    }

# Products endpoints
@app.get("/products", response_model=List[Product])
def get_products():
    """Get all products"""
    return list(db.products.values())

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Get specific product"""
    if product_id not in db.products:
        raise HTTPException(status_code=404, detail="Product not found")
    return db.products[product_id]

@app.post("/products", response_model=Product)
def create_product(product: Product):
    """Create new product"""
    if product.product_id in db.products:
        raise HTTPException(status_code=400, detail="Product already exists")
    db.products[product.product_id] = product
    return product

# Orders endpoints
@app.get("/orders", response_model=List[Order])
def get_orders():
    """Get all orders"""
    return db.orders

@app.post("/orders", response_model=Order)
def create_order(order: Order):
    """Create new order"""
    # Validate product exists and has stock
    if order.product_id not in db.products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = db.products[order.product_id]
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Calculate total
    order.total = product.price * order.quantity
    order.created_at = datetime.now()
    
    # Update stock
    product.stock -= order.quantity
    
    # Save order
    db.orders.append(order)
    
    return order

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    """Get specific order"""
    for order in db.orders:
        if order.order_id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

# Analytics endpoint
@app.get("/analytics")
def get_analytics():
    """Get platform analytics"""
    total_revenue = sum(o.total for o in db.orders)
    avg_order_value = total_revenue / len(db.orders) if db.orders else 0
    
    # Product sales
    product_sales = {}
    for order in db.orders:
        if order.product_id not in product_sales:
            product_sales[order.product_id] = {'quantity': 0, 'revenue': 0}
        product_sales[order.product_id]['quantity'] += order.quantity
        product_sales[order.product_id]['revenue'] += order.total
    
    return {
        "total_products": len(db.products),
        "total_orders": len(db.orders),
        "total_revenue": round(total_revenue, 2),
        "avg_order_value": round(avg_order_value, 2),
        "top_products": sorted(
            product_sales.items(),
            key=lambda x: x[1]['revenue'],
            reverse=True
        )[:5]
    }

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting E-commerce API on http://localhost:8000")
    print("📚 Docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
