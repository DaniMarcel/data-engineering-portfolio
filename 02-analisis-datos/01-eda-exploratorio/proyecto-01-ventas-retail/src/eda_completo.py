"""
Análisis Exploratorio de Datos (EDA) - E-commerce
==================================================

Este script realiza un análisis exploratorio completo de datos de ventas
usando pandas, matplotlib y seaborn.

Análisis incluidos:
- Estadísticas descriptivas
- Análisis de ventas por categoría/tiempo
- Análisis de clientes
- Detección de outliers
- Identificación de problemas de calidad
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class AnalisisEcommerce:
    """Clase principal para análisis EDA de datos de e-commerce."""
    
    def __init__(self):
        """Inicializa el analizador."""
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / 'data' / 'raw'
        self.output_path = self.base_path / 'output'
        self.graficos_path = self.output_path / 'graficos'
        
        # Crear directorios si no existen
        self.output_path.mkdir(exist_ok=True)
        self.graficos_path.mkdir(exist_ok=True)
        
        self.transacciones = None
        self.clientes = None
        self.productos = None
    
    def cargar_datos(self):
        """Carga todos los datasets."""
        print("📂 Cargando datasets...")
        
        try:
            self.transacciones = pd.read_csv(self.data_path / 'transacciones.csv')
            self.clientes = pd.read_csv(self.data_path / 'clientes.csv')
            self.productos = pd.read_csv(self.data_path / 'productos.csv')
            
            print(f"✅ Transacciones: {len(self.transacciones):,} registros")
            print(f"✅ Clientes: {len(self.clientes):,} registros")
            print(f"✅ Productos: {len(self.productos):,} registros")
            
            # Convertir fechas
            self.transacciones['fecha'] = pd.to_datetime(self.transacciones['fecha'])
            self.clientes['fecha_registro'] = pd.to_datetime(self.clientes['fecha_registro'])
            
            return True
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return False
    
    def resumen_inicial(self):
        """Muestra resumen inicial de los datos."""
        print("\n" + "="*80)
        print("📊 RESUMEN INICIAL DE DATOS")
        print("="*80)
        
        print("\n🔍 INFORMACIÓN DE TRANSACCIONES:")
        print(self.transacciones.info())
        
        print("\n📈 ESTADÍSTICAS DESCRIPTIVAS:")
        print(self.transacciones[['cantidad', 'precio_unitario', 'total', 'descuento_porcentaje']].describe())
    
    def calidad_datos(self):
        """Analiza la calidad de los datos."""
        print("\n" + "="*80)
        print("🔍 ANÁLISIS DE CALIDAD DE DATOS")
        print("="*80)
        
        # Valores faltantes
        print("\n📉 Valores Faltantes:")
        missing = self.transacciones.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            for col, count in missing.items():
                pct = (count / len(self.transacciones)) * 100
                print(f"   {col}: {count} ({pct:.2f}%)")
        else:
            print("   ✅ No hay valores faltantes")
        
        # Duplicados
        dup_count = self.transacciones.duplicated().sum()
        print(f"\n🔄 Registros Duplicados: {dup_count}")
        
        # Outliers en cantidad
        Q1 = self.transacciones['cantidad'].quantile(0.25)
        Q3 = self.transacciones['cantidad'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((self.transacciones['cantidad'] < Q1 - 1.5 * IQR) | 
                   (self.transacciones['cantidad'] > Q3 + 1.5 * IQR)).sum()
        print(f"📊 Outliers en cantidad: {outliers}")
        
        # Guardar reporte
        with open(self.output_path / 'calidad_datos.txt', 'w', encoding='utf-8') as f:
            f.write("REPORTE DE CALIDAD DE DATOS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Valores faltantes:\n{missing}\n\n")
            f.write(f"Duplicados: {dup_count}\n")
            f.write(f"Outliers en cantidad: {outliers}\n")
        
        print(f"\n💾 Reporte guardado en: {self.output_path / 'calidad_datos.txt'}")
    
    def analisis_ventas_tiempo(self):
        """Analiza ventas a lo largo del tiempo."""
        print("\n" + "="*80)
        print("📈 ANÁLISIS DE VENTAS POR TIEMPO")
        print("="*80)
        
        # Ventas por mes
        ventas_mes = self.transacciones.groupby('mes')['total'].agg(['sum', 'count', 'mean'])
        ventas_mes.columns = ['Total Ingresos', 'Num Transacciones', 'Ticket Promedio']
        print("\n📅 Ventas por Mes:")
        print(ventas_mes)
        
        # Gráfico de ventas por mes
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Ingresos mensuales
        ventas_mes['Total Ingresos'].plot(kind='bar', ax=axes[0, 0], color='steelblue')
        axes[0, 0].set_title('Ingresos Totales por Mes', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Mes')
        axes[0, 0].set_ylabel('Ingresos (€)')
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # 2. Número de transacciones
        ventas_mes['Num Transacciones'].plot(kind='bar', ax=axes[0, 1], color='coral')
        axes[0, 1].set_title('Número de Transacciones por Mes', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Mes')
        axes[0, 1].set_ylabel('Transacciones')
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # 3. Ventas por día de la semana
        ventas_dia = self.transacciones.groupby('dia_semana')['total'].sum().sort_values(ascending=False)
        ventas_dia.plot(kind='barh', ax=axes[1, 0], color='mediumseagreen')
        axes[1, 0].set_title('Ingresos por Día de la Semana', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Ingresos (€)')
        
        # 4. Tendencia temporal
        ventas_diaria = self.transacciones.groupby('fecha')['total'].sum()
        ventas_diaria.plot(ax=axes[1, 1], color='darkviolet', linewidth=2)
        axes[1, 1].set_title('Tendencia de Ingresos Diarios', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Fecha')
        axes[1, 1].set_ylabel('Ingresos (€)')
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.graficos_path / '01_ventas_tiempo.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Gráfico guardado: 01_ventas_tiempo.png")
        plt.close()
    
    def analisis_categorias(self):
        """Analiza ventas por categoría."""
        print("\n" + "="*80)
        print("📦 ANÁLISIS POR CATEGORÍAS")
        print("="*80)
        
        # Ventas por categoría
        ventas_cat = self.transacciones.groupby('categoria').agg({
            'total': ['sum', 'count'],
            'cantidad': 'sum',
            'descuento_porcentaje': 'mean'
        }).round(2)
        
        ventas_cat.columns = ['Ingresos', 'Transacciones', 'Unidades', 'Desc. Promedio']
        ventas_cat = ventas_cat.sort_values('Ingresos', ascending=False)
        print(ventas_cat)
        
        # Visualización
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Ingresos por categoría
        ventas_cat['Ingresos'].plot(kind='bar', ax=axes[0, 0], color='teal')
        axes[0, 0].set_title('Ingresos por Categoría', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('Ingresos (€)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Distribución (pie chart)
        axes[0, 1].pie(ventas_cat['Ingresos'], labels=ventas_cat.index, autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Distribución de Ingresos por Categoría', fontsize=14, fontweight='bold')
        
        # 3. Top 10 productos
        top_productos = self.transacciones.groupby('producto_nombre')['total'].sum().nlargest(10)
        top_productos.plot(kind='barh', ax=axes[1, 0], color='orange')
        axes[1, 0].set_title('Top 10 Productos Más Vendidos', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Ingresos (€)')
        
        # 4. Descuento promedio por categoría
        ventas_cat['Desc. Promedio'].plot(kind='bar', ax=axes[1, 1], color='crimson')
        axes[1, 1].set_title('Descuento Promedio por Categoría (%)', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('Descuento (%)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.graficos_path / '02_categorias.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Gráfico guardado: 02_categorias.png")
        plt.close()
    
    def analisis_clientes(self):
        """Analiza comportamiento de clientes."""
        print("\n" + "="*80)
        print("👥 ANÁLISIS DE CLIENTES")
        print("="*80)
        
        # Merge con clientes
        df = self.transacciones.merge(self.clientes, on='cliente_id', how='left')
        
        # Clientes top
        top_clientes = df.groupby('cliente_id').agg({
            'total': ['sum', 'count'],
            'nombre': 'first',
            'apellido': 'first',
            'segmento': 'first'
        }).round(2)
        
        top_clientes.columns = ['Total Gastado', 'Num Compras', 'Nombre', 'Apellido', 'Segmento']
        top_clientes = top_clientes.sort_values('Total Gastado', ascending=False).head(10)
        
        print("\n🏆 Top 10 Clientes:")
        print(top_clientes[['Nombre', 'Apellido', 'Total Gastado', 'Num Compras', 'Segmento']])
        
        # Análisis por segmento
        print("\n📊 Ventas por Segmento de Cliente:")
        segmento = df.groupby('segmento')['total'].agg(['sum', 'count', 'mean'])
        print(segmento)
        
        # Visualización
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # Ventas por segmento
        segmento['sum'].plot(kind='bar', ax=axes[0], color='navy')
        axes[0].set_title('Ingresos por Segmento', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Ingresos (€)')
        
        # Ventas por ciudad
        ventas_ciudad = df.groupby('ciudad')['total'].sum().nlargest(10)
        ventas_ciudad.plot(kind='barh', ax=axes[1], color='darkgreen')
        axes[1].set_title('Top 10 Ciudades por Ingresos', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Ingresos (€)')
        
        # Distribución de edad
        df['edad'].plot(kind='hist', bins=20, ax=axes[2], color='purple', edgecolor='black')
        axes[2].set_title('Distribución de Edad de Clientes', fontsize=14, fontweight='bold')
        axes[2].set_xlabel('Edad')
        axes[2].set_ylabel('Frecuencia')
        
        plt.tight_layout()
        plt.savefig(self.graficos_path / '03_clientes.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Gráfico guardado: 03_clientes.png")
        plt.close()
    
    def generar_reporte_completo(self):
        """Genera un reporte completo en formato texto."""
        reporte_path = self.output_path / 'reporte_eda.txt'
        
        with open(reporte_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("REPORTE DE ANÁLISIS EXPLORATORIO DE DATOS (EDA)\n")
            f.write("E-commerce - Ventas 2024\n")
            f.write("="*80 + "\n\n")
            
            f.write("RESUMEN EJECUTIVO\n")
            f.write("-"*80 + "\n")
            f.write(f"Total Transacciones: {len(self.transacciones):,}\n")
            f.write(f"Ingresos Totales: €{self.transacciones['total'].sum():,.2f}\n")
            f.write(f"Ticket Promedio: €{self.transacciones['total'].mean():.2f}\n")
            f.write(f"Período: {self.transacciones['fecha'].min()} a {self.transacciones['fecha'].max()}\n\n")
            
            # Más secciones...
            f.write("CATEGORÍAS PRINCIPALES\n")
            f.write("-"*80 + "\n")
            top_cat = self.transacciones.groupby('categoria')['total'].sum().nlargest(5)
            for cat, total in top_cat.items():
                f.write(f"{cat}: €{total:,.2f}\n")
        
        print(f"\n📝 Reporte completo guardado: {reporte_path}")
    
    def ejecutar_analisis_completo(self):
        """Ejecuta todo el análisis EDA."""
        print("="*80)
        print("🔍 ANÁLISIS EXPLORATORIO DE DATOS (EDA) - E-COMMERCE")
        print("="*80)
        
        if not self.cargar_datos():
            return
        
        self.resumen_inicial()
        self.calidad_datos()
        self.analisis_ventas_tiempo()
        self.analisis_categorias()
        self.analisis_clientes()
        self.generar_reporte_completo()
        
        print("\n" + "="*80)
        print("✨ ANÁLISIS COMPLETADO")
        print("="*80)
        print(f"\n📁 Resultados guardados en: {self.output_path}")
        print(f"📊 Gráficos guardados en: {self.graficos_path}")


if __name__ == "__main__":
    analisis = AnalisisEcommerce()
    analisis.ejecutar_analisis_completo()
