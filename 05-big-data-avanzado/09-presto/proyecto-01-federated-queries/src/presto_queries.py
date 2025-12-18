"""Presto Federated Query Example"""

# Simulates Presto distributed SQL queries

presto_queries = {
    "cross_source": """
-- Query across multiple data sources
SELECT 
    h.customer_id,
    h.order_date,
    h.total_amount,
    p.customer_name,
    p.email
FROM hive.sales.orders h
JOIN postgres.crm.customers p
    ON h.customer_id = p.customer_id
WHERE h.order_date >= DATE '2024-01-01';
""",
    
    "aggregation": """
-- Multi-source aggregation
SELECT 
    d.product_category,
    COUNT(DISTINCT m.customer_id) as unique_customers,
    SUM(m.revenue) as total_revenue
FROM mysql.products.dim_products d
JOIN mongodb.transactions.sales m
    ON d.product_id = m.product_id
GROUP BY d.product_category
ORDER BY total_revenue DESC;
""",
    
    "federation": """
-- Federated analytics
WITH aws_data AS (
    SELECT * FROM s3.datalake.events
    WHERE event_date = CURRENT_DATE
),
gcp_data AS (
    SELECT * FROM bigquery.warehouse.metrics
    WHERE metric_date = CURRENT_DATE
)
SELECT 
    a.event_type,
    COUNT(*) as event_count,
    AVG(g.value) as avg_metric
FROM aws_data a
LEFT JOIN gcp_data g
    ON a.event_id = g.event_id
GROUP BY a.event_type;
"""
}

print("🚀 PRESTO FEDERATED QUERIES\n")
print("Querying across: Hive, PostgreSQL, MySQL, MongoDB, S3, BigQuery\n")

for name, query in presto_queries.items():
    print(f"\n{'='*70}")
    print(f"Example: {name.upper()}")
    print(f"{'='*70}")
    print(query)

print("\n✅ Presto enables querying multiple data sources with one SQL!")
print("\nData Sources:")
print("  - Hive (Hadoop)")
print("  - PostgreSQL")
print("  - MySQL")  
print("  - MongoDB")
print("  - S3")
print("  - BigQuery")
