"""ETL Pipeline - Extract, Transform, Load"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

class EcommercePipeline:
    """Complete ETL pipeline for e-commerce data"""
    
    def __init__(self):
        self.data = None
        self.transformed_data = None
        
    def extract(self, source_path=None):
        """Extract data from source"""
        print("📥 EXTRACT: Loading data...")
        
        # Find data engineer base directory
        base = Path(__file__).resolve()
        for parent in base.parents:
            if parent.name == 'data engineer':
                data_path = parent / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw' / 'transacciones.csv'
                if data_path.exists():
                    self.data = pd.read_csv(data_path)
                    print(f"✅ Loaded {len(self.data):,} records from transactions")
                    return
        
        # Fallback: generate sample data
        print("⚠️  Source data not found, generating sample...")
        self.data = pd.DataFrame({
            'order_id': range(1000),
            'customer_id': [i % 100 for i in range(1000)],
            'product_id': [i % 5 + 1 for i in range(1000)],
            'quantity': [(i % 5) + 1 for i in range(1000)],
            'price': [50 + (i * 10) % 200 for i in range(1000)],
            'timestamp': [datetime.now() for _ in range(1000)]
        })
        print(f"✅ Generated {len(self.data):,} sample records")
    
    def transform(self):
        """Transform and clean data"""
        print("\n🔄 TRANSFORM: Processing data...")
        
        df = self.data.copy()
        
        # Calculate total
        df['total'] = df['quantity'] * df['price']
        
        # Add processing timestamp
        df['processed_at'] = datetime.now()
        
        # Clean nulls
        df = df.dropna()
        
        # Add categories
        category_map = {1: 'Electronics', 2: 'Accessories', 3: 'Electronics', 
                       4: 'Electronics', 5: 'Accessories'}
        df['category'] = df['product_id'].map(category_map)
        
        # Add status
        df['status'] = 'completed'
        
        self.transformed_data = df
        print(f"✅ Transformed {len(df):,} records")
        print(f"   Total Revenue: ${df['total'].sum():,.2f}")
        print(f"   Avg Order Value: ${df['total'].mean():.2f}")
        
        return df
    
    def load(self, output_dir='../data/processed'):
        """Load data to target"""
        print("\n💾 LOAD: Saving processed data...")
        
        output_path = Path(__file__).parent / output_dir
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as CSV
        csv_path = output_path / 'ecommerce_data.csv'
        self.transformed_data.to_csv(csv_path, index=False)
        print(f"✅ Saved CSV: {csv_path}")
        
        # Save as Parquet (more efficient)
        parquet_path = output_path / 'ecommerce_data.parquet'
        self.transformed_data.to_parquet(parquet_path, index=False)
        print(f"✅ Saved Parquet: {parquet_path}")
        
        # Save summary stats as JSON
        stats = {
            'total_records': len(self.transformed_data),
            'total_revenue': float(self.transformed_data['total'].sum()),
            'avg_order_value': float(self.transformed_data['total'].mean()),
            'processed_at': datetime.now().isoformat()
        }
        
        stats_path = output_path / 'summary_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"✅ Saved stats: {stats_path}")
        
        return csv_path
    
    def run(self):
        """Run complete ETL pipeline"""
        print("="*60)
        print("🔄 E-COMMERCE ETL PIPELINE")
        print("="*60)
        
        self.extract()
        self.transform()
        result = self.load()
        
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETED")
        print("="*60)
        
        return result

if __name__ == "__main__":
    pipeline = EcommercePipeline()
    pipeline.run()
