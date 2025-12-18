"""Spark ETL Pipeline"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when, date_format, to_date
from pathlib import Path

def create_spark():
    return SparkSession.builder \
        .appName("ETL Pipeline") \
        .master("local[*]") \
        .getOrCreate()

def extract(spark, data_path):
    """Extract data from CSV"""
    print("📥 EXTRACT")
    df = spark.read.csv(str(data_path), header=True, inferSchema=True)
    print(f"   Loaded: {df.count():,} rows")
    return df

def transform(df):
    """Transform data"""
    print("\n🔄 TRANSFORM")
    
    # Clean nulls
    df_clean = df.dropna()
    print(f"   After cleaning: {df_clean.count():,} rows")
    
    # Add calculated columns
    df_trans = df_clean.withColumn(
        "total_calculado",
        col("precio_unitario") * col("cantidad")
    )
    
    # Aggregate by category
    df_agg = df_trans.groupBy("categoria").agg(
        sum("total").alias("ingresos_totales"),
        avg("total").alias("ticket_promedio"),
        count("*").alias("num_transacciones")
    )
    
    return df_agg

def load(df, output_path):
    """Load data to Parquet"""
    print("\n💾 LOAD")
    df.write.mode("overwrite").parquet(str(output_path))
    print(f"   Saved to: {output_path}")

def main():
    print("="*70)
    print("⚡ SPARK ETL PIPELINE")
    print("="*70)
    
    spark = create_spark()
    
    # Paths
    # Buscar carpeta base \'data engineer\'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == \'data engineer\':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
    input_path = base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv'
    output_path = base_path / '05-big-data-avanzado/01-apache-spark/proyecto-02-spark-etl/output/ventas_agregadas.parquet'
    
    if input_path.exists():
        # ETL
        df_raw = extract(spark, input_path)
        df_transformed = transform(df_raw)
        df_transformed.show()
        load(df_transformed, output_path)
        
        print("\n✅ ETL Completed!")
    else:
        print("⚠️  Data not found. Generate data first.")
    
    spark.stop()

if __name__ == "__main__":
    main()
