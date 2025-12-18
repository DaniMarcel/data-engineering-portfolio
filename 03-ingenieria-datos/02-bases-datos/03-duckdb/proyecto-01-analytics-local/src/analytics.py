"""
Analytics Local con DuckDB
===========================

DuckDB es una base de datos OLAP (analytics) que:
- No requiere servidor (como SQLite)
- Optimizada para queries analíticas
- Lee directamente Parquet, CSV, JSON
- SQL completo con funciones de ventana
- Mucho más rápida que SQLite para analytics
"""

import duckdb
from pathlib import Path
import pandas as pd
from datetime import datetime

class DuckDBAnalytics:
    """Clase para analytics con DuckDB."""
    
    def __init__(self, db_path=':memory:'):
        """
        Inicializa conexión a DuckDB.
        
        Args:
            db_path (str): Ruta a la base de datos (':memory:' para en memoria)
        """
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self.# Buscar carpeta base \'data engineer\'
current_path = Path(__file__).resolve()
base_path = None
for parent in current_path.parents:
    if parent.name == \'data engineer\':
        base_path = parent
        break
if base_path is None:
    raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
        
        print(f"✅ Conexión a DuckDB establecida: {db_path}")
    
    def cargar_datos_e commerce(self):
        """Carga datos del proyecto EDA directamente."""
        data_path = self.base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw'
        
        print("\n📥 Cargando datos de e-commerce...")
        
        # DuckDB puede leer directamente archivos CSV y Parquet
        # Crear tablas desde archivos
        
        # 1. Transacciones desde Parquet (más rápido)
        parquet_file = str(data_path / 'transacciones.parquet')
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE transacciones AS 
            SELECT * FROM read_parquet('{parquet_file}')
        """)
        
        # 2. Clientes desde CSV
        clientes_file = str(data_path / 'clientes.csv')
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE clientes AS 
            SELECT * FROM read_csv_auto('{clientes_file}')
        """)
        
        # 3. Productos desde CSV
        productos_file = str(data_path / 'productos.csv')
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE productos AS 
            SELECT * FROM read_csv_auto('{productos_file}')
        """)
        
        # Verificar
        count_trans = self.conn.execute("SELECT COUNT(*) FROM transacciones").fetchone()[0]
        count_clientes = self.conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        count_productos = self.conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
        
        print(f"   ✅ Transacciones: {count_trans:,}")
        print(f"   ✅ Clientes: {count_clientes:,}")
        print(f"   ✅ Productos: {count_productos:,}")
    
    def query_ventas_por_mes(self):
        """Query: Ventas por mes."""
        print("\n" + "="*70)
        print("📊 VENTAS POR MES")
        print("="*70)
        
        query = """
        SELECT 
            mes,
            mes_nombre,
            COUNT(*) as num_transacciones,
            SUM(total) as ingresos_totales,
            AVG(total) as ticket_promedio,
            SUM(cantidad) as productos_vendidos
        FROM transacciones
        GROUP BY mes, mes_nombre
        ORDER BY mes
        """
        
        df = self.conn.execute(query).df()
        print(df.to_string(index=False))
        
        return df
    
    def query_top_productos(self, n=10):
        """Query: Top productos más vendidos."""
        print(f"\n" + "="*70)
        print(f"🏆 TOP {n} PRODUCTOS MÁS VENDIDOS")
        print("="*70)
        
        query = f"""
        SELECT 
            producto_nombre,
            categoria,
            COUNT(*) as num_ventas,
            SUM(cantidad) as unidades_vendidas,
            SUM(total) as ingresos_totales,
            AVG(precio_unitario) as precio_promedio
        FROM transacciones
        GROUP BY producto_nombre, categoria
        ORDER BY ingresos_totales DESC
        LIMIT {n}
        """
        
        df = self.conn.execute(query).df()
        print(df.to_string(index=False))
        
        return df
    
    def query_analisis_clientes(self):
        """Query: Análisis RFM simplificado."""
        print("\n" + "="*70)
        print("👥 ANÁLISIS DE CLIENTES (RFM Simplificado)")
        print("="*70)
        
        query = """
        WITH customer_metrics AS (
            SELECT 
                t.cliente_id,
                c.nombre,
                c.segmento,
                COUNT(*) as frecuencia,
                SUM(t.total) as valor_monetario,
                MAX(t.fecha) as ultima_compra
            FROM transacciones t
            JOIN clientes c ON t.cliente_id = c.cliente_id
            GROUP BY t.cliente_id, c.nombre, c.segmento
        )
        SELECT 
            segmento,
            COUNT(*) as num_clientes,
            AVG(frecuencia) as compras_promedio,
            AVG(valor_monetario) as gasto_promedio,
            SUM(valor_monetario) as ingreso_total
        FROM customer_metrics
        GROUP BY segmento
        ORDER BY ingreso_total DESC
        """
        
        df = self.conn.execute(query).df()
        print(df.to_string(index=False))
        
        return df
    
    def query_window_functions(self):
        """Query: Funciones de ventana - ranking de productos por categoría."""
        print("\n" + "="*70)
        print("🪟 FUNCIONES DE VENTANA - Ranking por Categoría")
        print("="*70)
        
        query = """
        WITH producto_ventas AS (
            SELECT 
                categoria,
                producto_nombre,
                SUM(total) as ingresos
            FROM transacciones
            GROUP BY categoria, producto_nombre
        )
        SELECT 
            categoria,
            producto_nombre,
            ingresos,
            ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY ingresos DESC) as ranking
        FROM producto_ventas
        QUALIFY ranking <= 3
        ORDER BY categoria, ranking
        """
        
        df = self.conn.execute(query).df()
        print(df.to_string(index=False))
        
        return df
    
    def query_tendencia_temporal(self):
        """Query: Tendencia de ventas con moving average."""
        print("\n" + "="*70)
        print("📈 TENDENCIA TEMPORAL CON MOVING AVERAGE")
        print("="*70)
        
        query = """
        WITH ventas_diarias AS (
            SELECT 
                fecha,
                SUM(total) as ingresos_dia
            FROM transacciones
            GROUP BY fecha
            ORDER BY fecha
        )
        SELECT 
            fecha,
            ingresos_dia,
            AVG(ingresos_dia) OVER (
                ORDER BY fecha 
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ) as moving_avg_7dias
        FROM ventas_diarias
        ORDER BY fecha DESC
        LIMIT 30
        """
        
        df = self.conn.execute(query).df()
        print(df.to_string(index=False))
        
        return df
    
    def query_cohort_analysis(self):
        """Query: Análisis de cohortes por mes de registro."""
        print("\n" + "="*70)
        print("📊 ANÁLISIS DE COHORTES")
        print("="*70)
        
        query = """
        WITH cliente_primera_compra AS (
            SELECT 
                cliente_id,
                MIN(fecha) as primera_compra,
                EXTRACT(MONTH FROM MIN(fecha)) as mes_cohorte
            FROM transacciones
            GROUP BY cliente_id
        )
        SELECT 
            c.mes_cohorte,
            COUNT(DISTINCT c.cliente_id) as clientes_en_cohorte,
            COUNT(DISTINCT t.transaccion_id) as total_transacciones,
            SUM(t.total) as ingresos_totales
        FROM cliente_primera_compra c
        LEFT JOIN transacciones t ON c.cliente_id = t.cliente_id
        GROUP BY c.mes_cohorte
        ORDER BY c.mes_cohorte
        """
        
        df = self.conn.execute(query).df()
        print(df.to_string(index=False))
        
        return df
    
    def exportar_resultados(self, df, nombre):
        """Exporta resultados a Parquet."""
        output_dir = Path(__file__).parent.parent / 'data'
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f'{nombre}.parquet'
        df.to_parquet(output_file)
        print(f"\n💾 Resultados guardados: {output_file}")
    
    def mostrar_info_db(self):
        """Muestra información de las tablas."""
        print("\n" + "="*70)
        print("📋 INFORMACIÓN DE LA BASE DE DATOS")
        print("="*70)
        
        # Listar tablas
        tables = self.conn.execute("SHOW TABLES").df()
        print("\nTablas disponibles:")
        print(tables.to_string(index=False))
        
        # Info de cada tabla
        for table in tables['name']:
            print(f"\n📊 Tabla: {table}")
            schema = self.conn.execute(f"DESCRIBE {table}").df()
            print(schema.to_string(index=False))
    
    def ejecutar_ejemplos(self):
        """Ejecuta todos los ejemplos."""
        print("="*70)
        print("🦆 ANALYTICS CON DUCKDB")
        print("="*70)
        
        # Cargar datos
        self.cargar_datos_ecommerce()
        
        # Info de DB
        self.mostrar_info_db()
        
        # Queries
        self.query_ventas_por_mes()
        self.query_top_productos(10)
        self.query_analisis_clientes()
        self.query_window_functions()
        self.query_tendencia_temporal()
        self.query_cohort_analysis()
        
        print("\n" + "="*70)
        print("✨ ANÁLISIS COMPLETADO")
        print("="*70)
    
    def close(self):
        """Cierra la conexión."""
        self.conn.close()
        print("\n🔒 Conexión cerrada")


def main():
    """Función principal."""
    # Crear analytics en memoria (más rápido)
    analytics = DuckDBAnalytics(':memory:')
    
    try:
        analytics.ejecutar_ejemplos()
    finally:
        analytics.close()


if __name__ == "__main__":
    main()
