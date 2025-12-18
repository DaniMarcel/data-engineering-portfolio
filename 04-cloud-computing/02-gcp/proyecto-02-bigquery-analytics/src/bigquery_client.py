"""GCP BigQuery Client Example"""
# Simulates BigQuery operations

import pandas as pd
from datetime import datetime

class BigQueryClient:
    """Simulated BigQuery client"""
    
    def __init__(self, project_id):
        self.project_id = project_id
        print(f"📊 Connected to project: {project_id}")
    
    def query(self, sql):
        """Execute SQL query"""
        print(f"\n🔍 Executing query:\n{sql}\n")
        
        # Simulate query result
        if "SELECT" in sql.upper():
            data = {
                'date': pd.date_range('2024-01-01', periods=5),
                'revenue': [1000, 1500, 1200, 1800, 2000],
                'transactions': [50, 75, 60, 90, 100]
            }
            df = pd.DataFrame(data)
            print("✅ Query executed successfully")
            return df
        
        print("✅ Query executed")
        return None
    
    def load_table(self, table_id, dataframe):
        """Load data to table"""
        print(f"\n💾 Loading {len(dataframe)} rows to {table_id}")
        print("✅ Load completed")
        return {'rows_loaded': len(dataframe)}

# Example usage
if __name__ == '__main__':
    print("🌩️  BIGQUERY ANALYTICS EXAMPLE\n")
    
    client = BigQueryClient('my-project')
    
    # Query
    sql = """
    SELECT date, SUM(revenue) as total_revenue
    FROM `project.dataset.sales`
    GROUP BY date
    ORDER BY date DESC
    LIMIT 5
    """
    
    results = client.query(sql)
    print("\n📊 Results:")
    print(results)
    
    # Load data
    new_data = pd.DataFrame({
        'product': ['A', 'B', 'C'],
        'sales': [100, 200, 150]
    })
    
    client.load_table('project.dataset.products', new_data)
    
    print("\n✅ BigQuery operations completed!")
