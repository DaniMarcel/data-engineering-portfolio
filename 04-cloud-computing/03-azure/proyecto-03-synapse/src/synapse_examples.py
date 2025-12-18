"""Azure Synapse Analytics Simulation"""

synapse_sql_examples = {
    "create_external_table": """
-- Create external table in Synapse
CREATE EXTERNAL TABLE dbo.sales (
    transaction_id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    transaction_date DATE
)
WITH (
    LOCATION = '/sales/',
    DATA_SOURCE = AzureDataLakeStore,
    FILE_FORMAT = ParquetFormat
);
""",
    
    "polybase_load": """
-- Load data using PolyBase
CREATE TABLE dbo.sales_staging
WITH (
    DISTRIBUTION = HASH(customer_id),
    CLUSTERED COLUMNSTORE INDEX
)
AS
SELECT *
FROM dbo.sales_external;
""",
    
    "analysis": """
-- Analytics query
SELECT 
    YEAR(transaction_date) as year,
    MONTH(transaction_date) as month,
    COUNT(*) as transaction_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_transaction
FROM dbo.sales
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY year DESC, month DESC;
"""
}

print("🏢 AZURE SYNAPSE ANALYTICS\n")
print("Modern cloud data warehouse\n")

for query_name, sql in synapse_sql_examples.items():
    print(f"{'='*60}")
    print(f"Example: {query_name.upper()}")
    print(f"{'='*60}")
    print(sql)
    print()

print("✅ Synapse SQL examples completed!")
print("\nFeatures:")
print("  - Massively parallel processing (MPP)")
print("  - PolyBase data loading")
print("  - Columnstore indexes")
print("  - Integration with Azure Data Lake")
