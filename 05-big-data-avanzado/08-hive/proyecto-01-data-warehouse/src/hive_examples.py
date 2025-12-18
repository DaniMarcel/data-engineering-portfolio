"""Hive SQL Data Warehouse Example"""

# Simulates Hive SQL operations

hive_sql_examples = {
    "create_table": """
-- Create external table
CREATE EXTERNAL TABLE IF NOT EXISTS sales (
    transaction_id INT,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2),
    transaction_date DATE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/data/warehouse/sales';
""",
    
    "load_data": """
-- Load data into partitioned table
INSERT INTO TABLE sales PARTITION (year=2024, month=1)
SELECT transaction_id, customer_id, product_id, amount, transaction_date
FROM staging.raw_sales
WHERE YEAR(transaction_date) = 2024 AND MONTH(transaction_date) = 1;
""",
    
    "analyze": """
-- Analytical query
SELECT 
    year,
    month,
    COUNT(*) as transaction_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_transaction
FROM sales
GROUP BY year, month
ORDER BY year DESC, month DESC;
"""
}

print("🐝 HIVE DATA WAREHOUSE EXAMPLE\n")

for query_type, sql in hive_sql_examples.items():
    print(f"\n{'='*60}")
    print(f"Query Type: {query_type.upper()}")
    print(f"{'='*60}")
    print(sql)

print("\n✅ Hive SQL examples completed!")
print("\nFeatures demonstrated:")
print("  - External tables")
print("  - Partitioning")
print("  - Parquet format")
print("  - Analytical queries")
