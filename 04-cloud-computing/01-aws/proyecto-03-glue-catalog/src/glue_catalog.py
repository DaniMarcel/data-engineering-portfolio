"""AWS Glue Data Catalog Simulation"""
import json
from datetime import datetime

class GlueDataCatalog:
    """Simulates AWS Glue Data Catalog"""
    
    def __init__(self):
        self.databases = {}
        self.tables = {}
    
    def create_database(self, name, description=''):
        """Create a Glue database"""
        self.databases[name] = {
            'Name': name,
            'Description': description,
            'CreateTime': datetime.now()
        }
        print(f"✅ Database '{name}' created")
    
    def create_table(self, database_name, table_name, columns, location):
        """Create a Glue table"""
        table_id = f"{database_name}.{table_name}"
        self.tables[table_id] = {
            'DatabaseName': database_name,
            'Name': table_name,
            'Columns': columns,
            'Location': location,
            'CreateTime': datetime.now()
        }
        print(f"✅ Table '{table_name}' created in database '{database_name}'")
    
    def get_table(self, database_name, table_name):
        """Retrieve table metadata"""
        table_id = f"{database_name}.{table_name}"
        if table_id in self.tables:
            return self.tables[table_id]
        return None

# Example usage
if __name__ == '__main__':
    print("📚 AWS GLUE DATA CATALOG SIMULATION\n")
    
    glue = GlueDataCatalog()
    
    # Create database
    glue.create_database('sales_db', 'Sales data warehouse')
    
    # Define table schema
    columns = [
        {'Name': 'transaction_id', 'Type': 'bigint'},
        {'Name': 'customer_id', 'Type': 'int'},
        {'Name': 'amount', 'Type': 'decimal(10,2)'},
        {'Name': 'transaction_date', 'Type': 'date'}
    ]
    
    # Create table
    glue.create_table(
        'sales_db',
        'transactions',
        columns,
        's3://my-data-lake/sales/transactions/'
    )
    
    # Retrieve metadata
    table = glue.get_table('sales_db', 'transactions')
    print(f"\n📊 Table Metadata:")
    print(json.dumps(table, indent=2, default=str))
    
    print("\n✅ Glue Data Catalog operations completed!")
    print(f"\nDatabases: {len(glue.databases)}")
    print(f"Tables: {len(glue.tables)}")
