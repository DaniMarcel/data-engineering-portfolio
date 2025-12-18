"""Complete E-commerce Data Platform
Integrates: FastAPI + ETL + Database + Dashboard
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import List, Dict, Optional

# ============= DATA MODELS =============

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float
    stock: int

class Order(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    timestamp: datetime

# ============= ETL PIPELINE =============

class EcommerceETL:
    """ETL Pipeline for e-commerce data"""
    
    def __init__(self):
        self.extracted_data = []
        self.transformed_data = []
    
    def extract(self, source_path: Optional[Path] = None):
        """Extract data from source"""
        if source_path and source_path.exists():
            df = pd.read_csv(source_path)
            self.extracted_data = df.to_dict('records')
        else:
            # Generate sample data
            self.extracted_data = [
                {'order_id': i, 'customer_id': i % 10, 'product_id': i % 5, 
                 'quantity': (i % 3) + 1, 'price': 100 + (i * 10) % 500}
                for i in range(50)
            ]
        
        print(f"✅ Extracted {len(self.extracted_data)} records")
        return len(self.extracted_data)
    
    def transform(self):
        """Transform and enrich data"""
        self.transformed_data = []
        
        for record in self.extracted_data:
            transformed = record.copy()
            transformed['total'] = record.get('quantity', 1) * record.get('price', 0)
            transformed['processed_at'] = datetime.now().isoformat()
            self.transformed_data.append(transformed)
        
        print(f"✅ Transformed {len(self.transformed_data)} records")
        return self.transformed_data
    
    def load(self, target_path='output/ecommerce_data.csv'):
        """Load data to target"""
        df = pd.DataFrame(self.transformed_data)
        Path(target_path).parent.mkdir(exist_ok=True)
        df.to_csv(target_path, index=False)
        print(f"✅ Loaded to {target_path}")
        return target_path

# ============= API =============

class EcommerceAPI:
    """FastAPI backend for e-commerce"""
    
    def __init__(self):
        self.app = FastAPI(title="E-commerce API")
        self.products = self._init_products()
        self.orders = []
        self._setup_routes()
    
    def _init_products(self):
        """Initialize product catalog"""
        return {
            1: Product(product_id=1, name="Laptop", category="Electronics", price=999.99, stock=10),
            2: Product(product_id=2, name="Mouse", category="Electronics", price=29.99, stock=50),
            3: Product(product_id=3, name="Keyboard", category="Electronics", price=79.99, stock=30),
        }
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        def root():
            return {"message": "E-commerce API", "endpoints": ["/products", "/orders", "/analytics"]}
        
        @self.app.get("/products")
        def get_products():
            return list(self.products.values())
        
        @self.app.get("/products/{product_id}")
        def get_product(product_id: int):
            if product_id not in self.products:
                raise HTTPException(status_code=404, detail="Product not found")
            return self.products[product_id]
        
        @self.app.post("/orders")
        def create_order(order: Order):
            self.orders.append(order)
            return {"status": "success", "order_id": order.order_id}
        
        @self.app.get("/analytics")
        def get_analytics():
            return {
                "total_products": len(self.products),
                "total_orders": len(self.orders),
                "total_revenue": sum(
                    self.products[o.product_id].price * o.quantity 
                    for o in self.orders if o.product_id in self.products
                )
            }

# ============= DASHBOARD =============

class EcommerceDashboard:
    """Analytics dashboard"""
    
    def __init__(self, data_path: Optional[str] = None):
        self.data = None
        if data_path and Path(data_path).exists():
            self.data = pd.read_csv(data_path)
    
    def show_metrics(self):
        """Display key metrics"""
        if self.data is None or len(self.data) == 0:
            print("📊 DASHBOARD: No data available")
            return
        
        print("\n" + "="*60)
        print("📊 E-COMMERCE DASHBOARD")
        print("="*60)
        
        print(f"\n📈 Key Metrics:")
        print(f"  Total Orders: {len(self.data):,}")
        print(f"  Total Revenue: ${self.data['total'].sum():,.2f}")
        print(f"  Avg Order Value: ${self.data['total'].mean():.2f}")
        
        if 'customer_id' in self.data.columns:
            print(f"  Unique Customers: {self.data['customer_id'].nunique()}")
        
        print(f"\n🏆 Top Products:")
        if 'product_id' in self.data.columns:
            top_products = self.data.groupby('product_id')['total'].sum().nlargest(3)
            for pid, revenue in top_products.items():
                print(f"  Product #{pid}: ${revenue:,.2f}")

# ============= INTEGRATION =============

def run_complete_platform():
    """Run the complete e-commerce platform"""
    print("🏪 E-COMMERCE COMPLETE PLATFORM")
    print("="*60)
    
    # 1. ETL Pipeline
    print("\n1️⃣ ETL PIPELINE")
    etl = EcommerceETL()
    
    # Try to load from existing data
    base = Path(__file__).resolve()
    for parent in base.parents:
        if parent.name == 'data engineer':
            data_path = parent / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw' / 'transacciones.csv'
            if data_path.exists():
                etl.extract(data_path)
                break
    else:
        etl.extract()  # Use sample data
    
    etl.transform()
    output_path = etl.load()
    
    # 2. API Backend
    print("\n2️⃣ API BACKEND")
    api = EcommerceAPI()
    print(f"✅ API initialized with {len(api.products)} products")
    
    # Simulate some orders
    from datetime import datetime
    for i in range(5):
        order = Order(
            order_id=i,
            customer_id=i % 3,
            product_id=(i % 3) + 1,
            quantity=i + 1,
            timestamp=datetime.now()
        )
        # Directly add orders (no HTTP call needed in simulation)
        api.orders.append(order)
    
    print(f"✅ Created {len(api.orders)} sample orders")
    
    analytics = {
        "total_products": len(api.products),
        "total_orders": len(api.orders),
        "total_revenue": sum(
            api.products[o.product_id].price * o.quantity 
            for o in api.orders
        )
    }
    print(f"📊 Revenue: ${analytics['total_revenue']:.2f}")
    
    # 3. Dashboard
    print("\n3️⃣ ANALYTICS DASHBOARD")
    dashboard = EcommerceDashboard(output_path)
    dashboard.show_metrics()
    
    print("\n" + "="*60)
    print("✅ PLATFORM COMPLETED")
    print("="*60)
    print("\nArchitecture:")
    print("  • FastAPI - REST backend")
    print("  • ETL Pipeline - Data processing")
    print("  • Dashboard - Analytics & reporting")
    print("\n💡 To run API server:")
    print("  uvicorn ecommerce_platform:api.app --reload")

if __name__ == "__main__":
    run_complete_platform()
