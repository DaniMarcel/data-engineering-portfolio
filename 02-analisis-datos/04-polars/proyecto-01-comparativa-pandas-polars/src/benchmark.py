"""
Comparativa Pandas vs Polars
=============================

Comparación de rendimiento y sintaxis entre pandas y polars para
operaciones comunes de análisis de datos.

Polars es una librería moderna para manipulación de datos que:
- Es más rápida que pandas (escrita en Rust)
- Usa lazy evaluation
- Optimiza automáticamente queries
- sintaxis similar a pandas pero más consistente
"""

import pandas as pd
import polars as pl
import time
from pathlib import Path
import numpy as np

class ComparativaPandasPolars:
    """Clase para comparar rendimiento de pandas vs polars."""
    
    def __init__(self):
        """Inicializa los paths."""
        # Buscar carpeta base 'data engineer'
        current_path = Path(__file__).resolve()
        base = None
        for parent in current_path.parents:
            if parent.name == 'data engineer':
                base = parent
                break
        if base is None:
            raise FileNotFoundError("No se pudo encontrar la carpeta base 'data engineer'")
        
        self.base_path = base
        self.data_path = base / '02-analisis-datos' / '01-eda-exploratorio' / 'proyecto-01-ventas-retail' / 'data' / 'raw'
        self.output_path = Path(__file__).parent.parent / 'output'
        self.output_path.mkdir(exist_ok=True)
        
        self.resultados = []
    
    def benchmark(self, nombre, func_pandas, func_polars):
        """
        Ejecuta benchmark de una operación.
        
        Args:
            nombre (str): Nombre de la operación
            func_pandas (callable): Función con pandas
            func_polars (callable): Función con polars
        """
        print(f"\n📊 {nombre}")
        print("-" * 60)
        
        # Pandas
        start = time.time()
        result_pandas = func_pandas()
        time_pandas = time.time() - start
        
        # Polars
        start = time.time()
        result_polars = func_polars()
        time_polars = time.time() - start
        
        # Calcular speedup
        speedup = time_pandas / time_polars if time_polars > 0 else 0
        
        print(f"⏱️  Pandas: {time_pandas:.4f}s")
        print(f"⏱️  Polars: {time_polars:.4f}s")
        print(f"🚀 Speedup: {speedup:.2f}x {'(Polars más rápido)' if speedup > 1 else '(Pandas más rápido)'}")
        
        self.resultados.append({
            'operacion': nombre,
            'tiempo_pandas': time_pandas,
            'tiempo_polars': time_polars,
            'speedup': speedup
        })
        
        return result_pandas, result_polars
    
    def test_01_lectura_csv(self):
        """Test: Lectura de archivo CSV."""
        csv_file = self.data_path / 'transacciones.csv'
        
        def leer_pandas():
            return pd.read_csv(csv_file)
        
        def leer_polars():
            return pl.read_csv(csv_file)
        
        df_pd, df_pl = self.benchmark("1. Lectura de CSV", leer_pandas, leer_polars)
        
        print(f"\n   📋 Pandas shape: {df_pd.shape}")
        print(f"   📋 Polars shape: {df_pl.shape}")
        
        return df_pd, df_pl
    
    def test_02_filtrado(self, df_pd, df_pl):
        """Test: Filtrado de datos."""
        
        def filtrar_pandas():
            return df_pd[df_pd['total'] > 100]
        
        def filtrar_polars():
            return df_pl.filter(pl.col('total') > 100)
        
        self.benchmark("2. Filtrado (total > 100)", filtrar_pandas, filtrar_polars)
    
    def test_03_groupby(self, df_pd, df_pl):
        """Test: Agregación con groupby."""
        
        def groupby_pandas():
            return df_pd.groupby('categoria')['total'].agg(['sum', 'mean', 'count'])
        
        def groupby_polars():
            return df_pl.group_by('categoria').agg([
                pl.col('total').sum().alias('sum'),
                pl.col('total').mean().alias('mean'),
                pl.col('total').count().alias('count')
            ])
        
        result_pd, result_pl = self.benchmark("3. GroupBy por categoría", groupby_pandas, groupby_polars)
        
        print(f"\n   Top 3 categorías (Pandas):")
        print(result_pd.sort_values('sum', ascending=False).head(3))
    
    def test_04_join(self, df_pd, df_pl):
        """Test: Join entre DataFrames."""
        # Cargar clientes
        clientes_pd = pd.read_csv(self.data_path / 'clientes.csv')
        clientes_pl = pl.read_csv(self.data_path / 'clientes.csv')
        
        def join_pandas():
            return df_pd.merge(clientes_pd, on='cliente_id', how='left')
        
        def join_polars():
            return df_pl.join(clientes_pl, on='cliente_id', how='left')
        
        result_pd, result_pl = self.benchmark("4. Join con clientes", join_pandas, join_polars)
        
        print(f"\n   📋 Resultado shape Pandas: {result_pd.shape}")
        print(f"   📋 Resultado shape Polars: {result_pl.shape}")
    
    def test_05_columnas_calculadas(self, df_pd, df_pl):
        """Test: Crear columnas calculadas."""
        
        def calcular_pandas():
            df = df_pd.copy()
            df['descuento_real'] = df['subtotal'] - df['total']
            df['margen'] = (df['total'] - df['monto_descuento']) / df['total'] * 100
            return df
        
        def calcular_polars():
            return df_pl.with_columns([
                (pl.col('subtotal') - pl.col('total')).alias('descuento_real'),
                ((pl.col('total') - pl.col('monto_descuento')) / pl.col('total') * 100).alias('margen')
            ])
        
        self.benchmark("5. Columnas calculadas", calcular_pandas, calcular_polars)
    
    def test_06_ordenamiento(self, df_pd, df_pl):
        """Test: Ordenamiento de datos."""
        
        def ordenar_pandas():
            return df_pd.sort_values('total', ascending=False)
        
        def ordenar_polars():
            return df_pl.sort('total', descending=True)
        
        self.benchmark("6. Ordenamiento por total", ordenar_pandas, ordenar_polars)
    
    def test_07_seleccion_columnas(self, df_pd, df_pl):
        """Test: Selección de columnas."""
        
        def seleccionar_pandas():
            return df_pd[['fecha', 'categoria', 'total', 'ciudad_envio']]
        
        def seleccionar_polars():
            return df_pl.select(['fecha', 'categoria', 'total', 'ciudad_envio'])
        
        self.benchmark("7. Selección de columnas", seleccionar_pandas, seleccionar_polars)
    
    def test_08_valores_unicos(self, df_pd, df_pl):
        """Test: Contar valores únicos."""
        
        def unicos_pandas():
            return df_pd['categoria'].nunique()
        
        def unicos_polars():
            return df_pl['categoria'].n_unique()
        
        self.benchmark("8. Valores únicos en categoría", unicos_pandas, unicos_polars)
    
    def mostrar_sintaxis(self):
        """Muestra comparativa de sintaxis."""
        print("\n" + "="*70)
        print("📖 COMPARATIVA DE SINTAXIS")
        print("="*70)
        
        ejemplos = [
            ("Lectura CSV", "pd.read_csv('file.csv')", "pl.read_csv('file.csv')"),
            ("Filtrado", "df[df['col'] > 10]", "df.filter(pl.col('col') > 10)"),
            ("GroupBy", "df.groupby('col').sum()", "df.group_by('col').sum()"),
            ("Join", "df1.merge(df2, on='id')", "df1.join(df2, on='id')"),
            ("Selección", "df[['col1', 'col2']]", "df.select(['col1', 'col2'])"),
            ("Nueva columna", "df['new'] = df['a'] + df['b']", "df.with_columns((pl.col('a') + pl.col('b')).alias('new'))"),
            ("Ordenar", "df.sort_values('col')", "df.sort('col')"),
        ]
        
        for nombre, sintaxis_pandas, sintaxis_polars in ejemplos:
            print(f"\n{nombre}:")
            print(f"   🐼 Pandas: {sintaxis_pandas}")
            print(f"   🐻‍❄️  Polars: {sintaxis_polars}")
    
    def guardar_resultados(self):
        """Guarda resultados del benchmark."""
        df_resultados = pd.DataFrame(self.resultados)
        
        # Guardar CSV
        csv_path = self.output_path / 'benchmark_results.csv'
        df_resultados.to_csv(csv_path, index=False)
        
        # Crear resumen
        resumen_path = self.output_path / 'resumen_benchmark.txt'
        with open(resumen_path, 'w', encoding='utf-8') as f:
            f.write("BENCHMARK PANDAS VS POLARS\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Total de tests: {len(self.resultados)}\n")
            f.write(f"Speedup promedio: {df_resultados['speedup'].mean():.2f}x\n")
            f.write(f"Speedup máximo: {df_resultados['speedup'].max():.2f}x\n")
            f.write(f"Speedup mínimo: {df_resultados['speedup'].min():.2f}x\n\n")
            
            f.write("RESULTADOS DETALLADOS\n")
            f.write("-"*70 + "\n\n")
            
            for _, row in df_resultados.iterrows():
                f.write(f"{row['operacion']}:\n")
                f.write(f"  Pandas: {row['tiempo_pandas']:.4f}s\n")
                f.write(f"  Polars: {row['tiempo_polars']:.4f}s\n")
                f.write(f"  Speedup: {row['speedup']:.2f}x\n\n")
        
        print(f"\n📁 Resultados guardados en: {self.output_path}")
        print(f"   - benchmark_results.csv")
        print(f"   - resumen_benchmark.txt")
    
    def ejecutar_todo(self):
        """Ejecuta todos los benchmarks."""
        print("="*70)
        print("🚀 COMPARATIVA PANDAS VS POLARS")
        print("="*70)
        
        # Cargar datos
        df_pd, df_pl = self.test_01_lectura_csv()
        
        # Tests
        self.test_02_filtrado(df_pd, df_pl)
        self.test_03_groupby(df_pd, df_pl)
        self.test_04_join(df_pd, df_pl)
        self.test_05_columnas_calculadas(df_pd, df_pl)
        self.test_06_ordenamiento(df_pd, df_pl)
        self.test_07_seleccion_columnas(df_pd, df_pl)
        self.test_08_valores_unicos(df_pd, df_pl)
        
        # Sintaxis
        self.mostrar_sintaxis()
        
        # Guardar
        self.guardar_resultados()
        
        print("\n" + "="*70)
        print("✨ BENCHMARK COMPLETADO")
        print("="*70)


def main():
    """Función principal."""
    comparativa = ComparativaPandasPolars()
    comparativa.ejecutar_todo()


if __name__ == "__main__":
    main()
