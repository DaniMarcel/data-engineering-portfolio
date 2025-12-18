"""Spark MLlib - Machine Learning"""
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

spark = SparkSession.builder.appName("ML").master("local[*]").getOrCreate()

# Sample data
data = [(1.0, 100.0), (2.0, 200.0), (3.0, 300.0), (4.0, 400.0)]
df = spark.createDataFrame(data, ["feature", "label"])

# Prepare features
assembler = VectorAssembler(inputCols=["feature"], outputCol="features")
df_features = assembler.transform(df)

# Train model
lr = LinearRegression(featuresCol="features", labelCol="label")
model = lr.fit(df_features)

print(f"✅ Model trained!")
print(f"Coefficients: {model.coefficients}")
print(f"Intercept: {model.intercept}")
print(f"RMSE: {model.summary.rootMeanSquaredError}")

spark.stop()
