"""Delta Lake Example with PySpark"""
from pyspark.sql import SparkSession
from delta import *

# Create Spark session with Delta Lake
builder = SparkSession.builder \
    .appName("DeltaLakeExample") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Sample data
data = [
    (1, "Product A", 100),
    (2, "Product B", 200),
    (3, "Product C", 150)
]

df = spark.createDataFrame(data, ["id", "name", "price"])

# Write as Delta table
delta_path = "delta-table"
df.write.format("delta").mode("overwrite").save(delta_path)

print("✅ Delta table created")

# Read Delta table
df_read = spark.read.format("delta").load(delta_path)
print("\n📊 Data from Delta Lake:")
df_read.show()

# ACID update
updatesDf = spark.createDataFrame([(2, "Product B Updated", 250)], ["id", "name", "price"])
updatesDf.write.format("delta").mode("append").save(delta_path)

print("\n✅ Data updated (ACID transactions)")

spark.stop()
