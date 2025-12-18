"""
Introducción a PySpark
=======================

Primeros pasos con Apache Spark usando PySpark.
Operaciones básicas con DataFrames distribuidos.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pathlib import Path

def crear_spark_session():
    """Crea sesión de Spark."""
    spark = SparkSession.builder \
        .appName("Intro PySpark") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    print(f"✅ Spark Session creada: {spark.version}")
    return spark


def ejemplo_basico(spark):
    """Ejemplo básico de DataFrame."""
    print("\n" + "="*70)
    print("📊 EJEMPLO BÁSICO: DATAFRAME")
    print("="*70)
    
    # Crear DataFrame desde Python list
    data = [
        ("Juan", 25, 50000),
        ("Ana", 30, 60000),
        ("Carlos", 28, 55000),
        ("María", 32, 65000)
    ]
    
    schema = ["nombre", "edad", "salario"]
    df = spark.createDataFrame(data, schema)
    
    print("\n📋 DataFrame creado:")
    df.show()
    
    print("\n🔍 Schema:")
    df.printSchema()
    
    # Operaciones básicas
    print("\n📊 Salario promedio:")
    df.select(avg("salario")).show()
    
    print("\n🔎 Filtrar edad > 28:")
    df.filter(col("edad") > 28).show()


def ejemplo_lectura_csv(spark):
    """Leer CSV con Spark."""
    print("\n" + "="*70)
    print("📥 EJEMPLO: LECTURA DE CSV")
    print("="*70)
    
    # Intentar cargar datos del proyecto EDA
    # Buscar carpeta base \'data engineer\'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == \'data engineer\':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
    csv_path = base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv'
    
    if csv_path.exists():
        df = spark.read.csv(str(csv_path), header=True, inferSchema=True)
        
        print(f"\n✅ Datos cargados: {df.count():,} filas")
        print("\n📋 Primeras filas:")
        df.show(5)
        
        print("\n📊 Estadísticas básicas:")
        df.describe("total", "cantidad").show()
    else:
        print("\n⚠️  CSV de ejemplo no encontrado")


def ejemplo_transformaciones(spark):
    """Transformaciones con Spark."""
    print("\n" + "="*70)
    print("🔄 EJEMPLO: TRANSFORMACIONES")
    print("="*70)
    
    # Datos de ventas
    data = [
        ("Laptop", "Electrónica", 1200, 5),
        ("Mouse", "Electrónica", 25, 20),
        ("Silla", "Hogar", 150, 10),
        ("Mesa", "Hogar", 300, 5),
        ("Monitor", "Electrónica", 400, 8),
    ]
    
    df = spark.createDataFrame(data, ["producto", "categoria", "precio", "cantidad"])
    
    print("\n📋 Datos originales:")
    df.show()
    
    # Calcular total
    df_con_total = df.withColumn("total", col("precio") * col("cantidad"))
    
    print("\n💰 Con columna total:")
    df_con_total.show()
    
    # GroupBy
    print("\n📊 Ventas por categoría:")
    df_con_total.groupBy("categoria") \
        .agg(
            sum("total").alias("total_ventas"),
            avg("precio").alias("precio_promedio"),
            count("*").alias("num_productos")
        ).show()


def ejemplo_sql(spark):
    """Usar SQL con Spark."""
    print("\n" + "="*70)
    print("🗄️  EJEMPLO: SPARK SQL")
    print("="*70)
    
    data = [
        ("Juan", "Madrid", 1000),
        ("Ana", "Barcelona", 1500),
        ("Carlos", "Madrid", 1200),
        ("María", "Valencia", 1100),
    ]
    
    df = spark.createDataFrame(data, ["nombre", "ciudad", "ventas"])
    
    # Registrar como tabla temporal
    df.createOrReplaceTempView("ventas")
    
    # Usar SQL
    print("\n📊 Query SQL:")
    resultado = spark.sql("""
        SELECT ciudad, 
               SUM(ventas) as total_ventas,
               COUNT(*) as num_vendedores
        FROM ventas
        GROUP BY ciudad
        ORDER BY total_ventas DESC
    """)
    
    resultado.show()


def main():
    """Función principal."""
    print("="*70)
    print("⚡ INTRODUCCIÓN A PYSPARK")
    print("="*70)
    
    # Crear sesión
    spark = crear_spark_session()
    
    try:
        # Ejemplos
        ejemplo_basico(spark)
        ejemplo_transformaciones(spark)
        ejemplo_sql(spark)
        ejemplo_lectura_csv(spark)
        
        print("\n" + "="*70)
        print("✨ EJEMPLOS COMPLETADOS")
        print("="*70)
        print("\n💡 PySpark permite:")
        print("   - Procesar datos distribuidos")
        print("   - Operaciones lazy evaluation")
        print("   - SQL sobre DataFrames")
        print("   - Escalabilidad horizontal")
        
    finally:
        spark.stop()
        print("\n🔒 Spark Session cerrada")


if __name__ == "__main__":
    main()
