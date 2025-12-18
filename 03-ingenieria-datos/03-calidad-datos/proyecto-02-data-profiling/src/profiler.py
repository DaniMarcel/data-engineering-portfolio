"""
Data Profiling - Análisis de Calidad de Datos
==============================================

Genera perfiles de datos completos con:
- Estadísticas descriptivas
- Detección de anomalías
- Valores únicos y frecuencias
- Correlaciones
- Reportes HTML
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


class DataProfiler:
    """Generador de perfiles de datos."""
    
    def __init__(self, df: pd.DataFrame, nombre_dataset: str = "Dataset"):
        """
        Inicializa el profiler.
        
        Args:
            df: DataFrame a analizar
            nombre_dataset: Nombre descriptivo del dataset
        """
        self.df = df.copy()
        self.nombre = nombre_dataset
        self.reporte = {
            'nombre': nombre_dataset,
            'fecha_analisis': datetime.now().isoformat(),
            'resumen': {},
            'columnas': {},
            'calidad': {},
            'correlaciones': {}
        }
    
    def analizar_resumen_general(self):
        """Genera resumen general del dataset."""
        print(f"\n{'='*80}")
        print(f"📊 PERFIL DE DATOS: {self.nombre}")
        print(f"{'='*80}")
        
        self.reporte['resumen'] = {
            'filas': len(self.df),
            'columnas': len(self.df.columns),
            'tamano_memoria_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'duplicados': self.df.duplicated().sum(),
            'pct_duplicados': (self.df.duplicated().sum() / len(self.df)) * 100
        }
        
        print(f"\n📈 Resumen General:")
        print(f"   Filas: {self.reporte['resumen']['filas']:,}")
        print(f"   Columnas: {self.reporte['resumen']['columnas']}")
        print(f"   Memoria: {self.reporte['resumen']['tamano_memoria_mb']:.2f} MB")
        print(f"   Duplicados: {self.reporte['resumen']['duplicados']:,} "
              f"({self.reporte['resumen']['pct_duplicados']:.2f}%)")
    
    def analizar_columna(self, col_name: str):
        """Analiza una columna en detalle."""
        col = self.df[col_name]
        
        perfil = {
            'nombre': col_name,
            'tipo': str(col.dtype),
            'no_nulos': col.notna().sum(),
            'nulos': col.isna().sum(),
            'pct_nulos': (col.isna().sum() / len(col)) * 100,
            'unicos': col.nunique(),
            'pct_unicos': (col.nunique() / len(col)) * 100
        }
        
        # Estadísticas según tipo
        if pd.api.types.is_numeric_dtype(col):
            perfil['estadisticas'] = {
                'min': float(col.min()) if col.notna().any() else None,
                'max': float(col.max()) if col.notna().any() else None,
                'mean': float(col.mean()) if col.notna().any() else None,
                'median': float(col.median()) if col.notna().any() else None,
                'std': float(col.std()) if col.notna().any() else None,
                'q25': float(col.quantile(0.25)) if col.notna().any() else None,
                'q75': float(col.quantile(0.75)) if col.notna().any() else None
            }
            
            # Detectar outliers (IQR method)
            if col.notna().any():
                Q1 = col.quantile(0.25)
                Q3 = col.quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((col < Q1 - 1.5 * IQR) | (col > Q3 + 1.5 * IQR)).sum()
                perfil['outliers'] = int(outliers)
                perfil['pct_outliers'] = (outliers / len(col)) * 100
        
        elif pd.api.types.is_string_dtype(col) or pd.api.types.is_object_dtype(col):
            # Top valores más frecuentes
            top_values = col.value_counts().head(10)
            perfil['top_10_valores'] = {
                str(k): int(v) for k, v in top_values.items()
            }
            
            # Longitud de strings
            if col.dtype == 'object':
                lengths = col.astype(str).str.len()
                perfil['longitud'] = {
                    'min': int(lengths.min()) if lengths.notna().any() else None,
                    'max': int(lengths.max()) if lengths.notna().any() else None,
                    'mean': float(lengths.mean()) if lengths.notna().any() else None
                }
        
        self.reporte['columnas'][col_name] = perfil
        
        return perfil
    
    def analizar_todas_columnas(self):
        """Analiza todas las columnas."""
        print(f"\n📋 Analizando {len(self.df.columns)} columnas...")
        
        for col in self.df.columns:
            self.analizar_columna(col)
        
        print(f"   ✅ Análisis completado")
    
    def analizar_calidad(self):
        """Analiza calidad de datos."""
        print(f"\n🔍 Análisis de Calidad de Datos:")
        print(f"{'='*80}")
        
        # Completitud
        completitud = {}
        for col in self.df.columns:
            pct_completo = (self.df[col].notna().sum() / len(self.df)) * 100
            completitud[col] = pct_completo
            
            if pct_completo < 90:
                print(f"   ⚠️  {col}: {pct_completo:.1f}% completo")
        
        self.reporte['calidad']['completitud'] = completitud
        
        # Unicidad (para columnas que deberían ser únicas)
        print(f"\n🔑 Análisis de Unicidad:")
        for col in self.df.columns:
            if 'id' in col.lower():
                pct_unico = (self.df[col].nunique() / len(self.df)) * 100
                if pct_unico < 100:
                    print(f"   ⚠️  {col}: {pct_unico:.1f}% único "
                          f"({len(self.df) - self.df[col].nunique()} duplicados)")
    
    def analizar_correlaciones(self):
        """Analiza correlaciones entre variables numéricas."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 1:
            print(f"\n📊 Correlaciones (variables numéricas):")
            print(f"{'='*80}")
            
            corr_matrix = self.df[numeric_cols].corr()
            
            # Encontrar correlaciones fuertes
            correlaciones_fuertes = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    corr = corr_matrix.iloc[i, j]
                    
                    if abs(corr) > 0.7:
                        correlaciones_fuertes.append({
                            'col1': col1,
                            'col2': col2,
                            'correlacion': float(corr)
                        })
                        print(f"   {col1} ↔ {col2}: {corr:.3f}")
            
            self.reporte['correlaciones'] = correlaciones_fuertes
    
    def generar_reporte_consola(self):
        """Genera reporte en consola."""
        print(f"\n{'='*80}")
        print(f"📋 REPORTE DETALLADO POR COLUMNA")
        print(f"{'='*80}")
        
        for col_name, perfil in self.reporte['columnas'].items():
            print(f"\n📊 {col_name}")
            print(f"   Tipo: {perfil['tipo']}")
            print(f"   Nulos: {perfil['nulos']:,} ({perfil['pct_nulos']:.2f}%)")
            print(f"   Únicos: {perfil['unicos']:,} ({perfil['pct_unicos']:.2f}%)")
            
            if 'estadisticas' in perfil:
                est = perfil['estadisticas']
                print(f"   Rango: [{est['min']:.2f}, {est['max']:.2f}]")
                print(f"   Media: {est['mean']:.2f} ± {est['std']:.2f}")
                print(f"   Mediana: {est['median']:.2f}")
                if 'outliers' in perfil:
                    print(f"   Outliers: {perfil['outliers']:,} ({perfil['pct_outliers']:.2f}%)")
            
            if 'top_10_valores' in perfil and len(perfil['top_10_valores']) <= 10:
                print(f"   Top valores:")
                for val, count in list(perfil['top_10_valores'].items())[:5]:
                    print(f"      {val}: {count:,}")
    
    def guardar_reporte_json(self, output_path: Path):
        """Guarda reporte en JSON."""
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.reporte, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reporte guardado: {output_path}")
    
    def generar_perfil_completo(self, output_dir: Path = None):
        """Genera perfil completo."""
        self.analizar_resumen_general()
        self.analizar_todas_columnas()
        self.analizar_calidad()
        self.analizar_correlaciones()
        self.generar_reporte_consola()
        
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)
            
            # Guardar JSON
            json_path = output_dir / f'perfil_{self.nombre}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            self.guardar_reporte_json(json_path)


def main():
    """Función principal."""
    print("="*80)
    print("🔍 DATA PROFILING - ANÁLISIS DE CALIDAD")
    print("="*80)
    
    # Cargar datos de ejemplo
    # Buscar carpeta base \'data engineer\'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == \'data engineer\':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
    data_path = base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw'
    
    try:
        df = pd.read_csv(data_path / 'transacciones.csv')
        print(f"\n✅ Datos cargados: {len(df):,} transacciones")
        
        # Crear profiler
        profiler = DataProfiler(df, "Transacciones E-commerce")
        
        # Generar perfil
        output_dir = Path(__file__).parent.parent / 'reports'
        profiler.generar_perfil_completo(output_dir)
        
        print("\n" + "="*80)
        print("✨ PROFILING COMPLETADO")
        print("="*80)
        
    except FileNotFoundError:
        print("\n⚠️  Datos no encontrados. Ejecuta primero el generador de datos del proyecto EDA")


if __name__ == "__main__":
    main()
