"""Visualización Avanzada con Matplotlib y Seaborn"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def cargar_datos():
    # Buscar carpeta base \'data engineer\'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == \'data engineer\':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
    data_path = base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv'
    return pd.read_csv(data_path)

def crear_subplot_complejo():
    """Subplot con múltiples gráficos"""
    df = cargar_datos()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Dashboard de Ventas - Análisis Completo', fontsize=16, fontweight='bold')
    
    # 1. Distribución de ventas
    axes[0, 0].hist(df['total'], bins=50, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribución de Ventas')
    axes[0, 0].set_xlabel('Total (€)')
    axes[0, 0].set_ylabel('Frecuencia')
    
    # 2. Boxplot por categoría
    df.boxplot(column='total', by='categoria', ax=axes[0, 1])
    axes[0, 1].set_title('Ventas por Categoría')
    axes[0, 1].set_xlabel('Categoría')
    
    # 3. Heatmap de correlaciones
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[1, 0])
    axes[1, 0].set_title('Correlaciones')
    
    # 4. Top productos
    top = df.groupby('producto_nombre')['total'].sum().nlargest(10)
    axes[1, 1].barh(range(len(top)), top.values, color='coral')
    axes[1, 1].set_yticks(range(len(top)))
    axes[1, 1].set_yticklabels(top.index)
    axes[1, 1].set_title('Top 10 Productos')
    
    plt.tight_layout()
    plt.savefig('dashboard_completo.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard saved: dashboard_completo.png")

def crear_grafico_profesional():
    """Gráfico profesional con anotaciones"""
    df = cargar_datos()
    df['fecha'] = pd.to_datetime(df['fecha'])
    ventas_diarias = df.groupby('fecha')['total'].sum()
    
    plt.figure(figsize=(14, 6))
    plt.plot(ventas_diarias.index, ventas_diarias.values, 
             linewidth=2, color='#2E86AB', marker='o', markersize=4)
    
    # Anotar máximo
    max_val = ventas_diarias.max()
    max_date = ventas_diarias.idxmax()
    plt.annotate(f'Máximo: €{max_val:,.0f}',
                xy=(max_date, max_val),
                xytext=(10, 20),
                textcoords='offset points',
                bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', color='red'))
    
    plt.title('Evolución de Ventas Diarias', fontsize=16, fontweight='bold')
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Ingresos (€)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('ventas_profesional.png', dpi=300, bbox_inches='tight')
    print("✅ Chart saved: ventas_profesional.png")

if __name__ == "__main__":
    print("🎨 Generando visualizaciones avanzadas...")
    crear_subplot_complejo()
    crear_grafico_profesional()
    print("\n✨ Completado!")
