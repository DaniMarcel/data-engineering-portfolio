"""
Visualizaciones Interactivas con Plotly
========================================

Plotly permite crear gráficos interactivos de alta calidad con:
- Zoom, pan, hover tooltips
- Export a PNG/SVG
- Gráficos 3D
- Mapas
- Subplots complejos
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path

class PlotlyVisualizer:
    """Clase para crear visualizaciones con Plotly."""
    
    def __init__(self):
        """Inicializa el visualizador."""
        self.# Buscar carpeta base \'data engineer\'
current_path = Path(__file__).resolve()
base_path = None
for parent in current_path.parents:
    if parent.name == \'data engineer\':
        base_path = parent
        break
if base_path is None:
    raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
        self.data_path = self.base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw'
        self.output_path = Path(__file__).parent.parent / 'output'
        self.output_path.mkdir(exist_ok=True)
        
        # Cargar datos
        self.df = pd.read_csv(self.data_path / 'transacciones.csv')
        self.df['fecha'] = pd.to_datetime(self.df['fecha'])
        
        print(f"✅ Datos cargados: {len(self.df):,} transacciones")
    
    def grafico_01_linea_interactiva(self):
        """Gráfico de línea interactivo con múltiples series."""
        print("\n📈 Creando gráfico de línea interactivo...")
        
        # Preparar datos
        ventas_dia = self.df.groupby('fecha')['total'].agg(['sum', 'mean', 'count']).reset_index()
        
        # Crear figura con subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Ingresos Diarios', 'Número de Transacciones'),
            vertical_spacing=0.15
        )
        
        # First subplot: Ingresos
        fig.add_trace(
            go.Scatter(
                x=ventas_dia['fecha'],
                y=ventas_dia['sum'],
                mode='lines+markers',
                name='Ingresos Totales',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4),
                hovertemplate='<b>%{x}</b><br>Ingresos: €%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Second subplot: Transacciones
        fig.add_trace(
            go.Scatter(
                x=ventas_dia['fecha'],
                y=ventas_dia['count'],
                mode='lines',
                name='Transacciones',
                line=dict(color='#ff7f0e', width=2),
                fill='tozeroy',
                hovertemplate='<b>%{x}</b><br>Transacciones: %{y}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_xaxes(title_text="Fecha", row=2, col=1)
        fig.update_yaxes(title_text="Ingresos (€)", row=1, col=1)
        fig.update_yaxes(title_text="Transacciones", row=2, col=1)
        
        fig.update_layout(
            title='Análisis Temporal de Ventas',
            height=700,
            showlegend=True,
            hovermode='x unified'
        )
        
        # Guardar
        fig.write_html(self.output_path / '01_linea_interactiva.html')
        print(f"   ✅ Guardado: 01_linea_interactiva.html")
        
        return fig
    
    def grafico_02_barras_agrupadas(self):
        """Gráfico de barras agrupadas."""
        print("\n📊 Creando gráfico de barras agrupadas...")
        
        # Datos: Ventas por categoría y canal
        df_grouped = self.df.groupby(['categoria', 'canal'])['total'].sum().reset_index()
        
        fig = px.bar(
            df_grouped,
            x='categoria',
            y='total',
            color='canal',
            title='Ingresos por Categoría y Canal',
            labels={'total': 'Ingresos (€)', 'categoria': 'Categoría', 'canal': 'Canal'},
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_layout(
            hovermode='x unified',
            height=600
        )
        
        fig.write_html(self.output_path / '02_barras_agrupadas.html')
        print(f"   ✅ Guardado: 02_barras_agrupadas.html")
        
        return fig
    
    def grafico_03_sunburst(self):
        """Gráfico sunburst (jerárquico)."""
        print("\n☀️  Creando gráfico sunburst...")
        
        # Agregar datos para jerarquía
        df_sunburst = self.df.groupby(['categoria', 'subcategoria'])['total'].sum().reset_index()
        
        fig = px.sunburst(
            df_sunburst,
            path=['categoria', 'subcategoria'],
            values='total',
            title='Distribución Jerárquica de Ventas',
            color='total',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(height=700)
        
        fig.write_html(self.output_path / '03_sunburst.html')
        print(f"   ✅ Guardado: 03_sunburst.html")
        
        return fig
    
    def grafico_04_scatter_3d(self):
        """Gráfico scatter 3D."""
        print("\n🌐 Creando gráfico scatter 3D...")
        
        # Agregar por producto
        df_productos = self.df.groupby('producto_nombre').agg({
            'cantidad': 'sum',
            'total': 'sum',
            'transaccion_id': 'count',
            'categoria': 'first'
        }).reset_index()
        
        df_productos.columns = ['producto', 'unidades', 'ingresos', 'num_ventas', 'categoria']
        
        # Top 50 productos
        df_top = df_productos.nlargest(50, 'ingresos')
        
        fig = px.scatter_3d(
            df_top,
            x='unidades',
            y='ingresos',
            z='num_ventas',
            color='categoria',
            size='ingresos',
            hover_name='producto',
            title='Análisis 3D de Productos (Top 50)',
            labels={
                'unidades': 'Unidades Vendidas',
                'ingresos': 'Ingresos (€)',
                'num_ventas': 'Número de Ventas'
            }
        )
        
        fig.update_layout(height=700)
        
        fig.write_html(self.output_path / '04_scatter_3d.html')
        print(f"   ✅ Guardado: 04_scatter_3d.html")
        
        return fig
    
    def grafico_05_heatmap_calendario(self):
        """Heatmap estilo calendario."""
        print("\n🗓️  Creando heatmap calendario...")
        
        # Preparar datos
        self.df['dia_semana'] = self.df['fecha'].dt.day_name()
        self.df['semana'] = self.df['fecha'].dt.isocalendar().week
        
        heatmap_data = self.df.groupby(['semana', 'dia_semana'])['total'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='dia_semana', columns='semana', values='total')
        
        # Ordenar días
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(dias_orden)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            colorscale='YlOrRd',
            hoverongaps=False,
            hovertemplate='Semana %{x}<br>%{y}<br>Ingresos: €%{z:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Heatmap de Ventas por Día y Semana del Año',
            xaxis_title='Semana del Año',
            yaxis_title='Día de la Semana',
            height=500
        )
        
        fig.write_html(self.output_path / '05_heatmap_calendario.html')
        print(f"   ✅ Guardado: 05_heatmap_calendario.html")
        
        return fig
    
    def grafico_06_funnel(self):
        """Gráfico de embudo."""
        print("\n🎯 Creando gráfico de embudo...")
        
        # Simular funnel de conversión
        funnel_data = {
            'Etapa': ['Visitas', 'Agregaron al Carrito', 'Iniciaron Checkout', 'Completaron Compra'],
            'Cantidad': [100000, 50000, 30000, len(self.df)]
        }
        
        fig = go.Figure(go.Funnel(
            y=funnel_data['Etapa'],
            x=funnel_data['Cantidad'],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(color=["deepskyblue", "lightsalmon", "tan", "mediumseagreen"])
        ))
        
        fig.update_layout(
            title='Embudo de Conversión E-commerce',
            height=600
        )
        
        fig.write_html(self.output_path / '06_funnel.html')
        print(f"   ✅ Guardado: 06_funnel.html")
        
        return fig
    
    def grafico_07_box_violins(self):
        """Box plots y violin plots."""
        print("\n🎻 Creando box y violin plots...")
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Box Plot', 'Violin Plot')
        )
        
        # Box plot
        for categoria in self.df['categoria'].unique():
            df_cat = self.df[self.df['categoria'] == categoria]
            fig.add_trace(
                go.Box(
                    y=df_cat['total'],
                    name=categoria,
                    showlegend=False
                ),
                row=1, col=1
            )
        
        # Violin plot
        for categoria in self.df['categoria'].unique():
            df_cat = self.df[self.df['categoria'] == categoria]
            fig.add_trace(
                go.Violin(
                    y=df_cat['total'],
                    name=categoria,
                    box_visible=True,
                    meanline_visible=True
                ),
                row=1, col=2
            )
        
        fig.update_yaxes(title_text="Total de Venta (€)", row=1, col=1)
        fig.update_yaxes(title_text="Total de Venta (€)", row=1, col=2)
        
        fig.update_layout(
            title='Distribución de Ventas por Categoría',
            height=600,
            showlegend=True
        )
        
        fig.write_html(self.output_path / '07_box_violin.html')
        print(f"   ✅ Guardado: 07_box_violin.html")
        
        return fig
    
    def crear_dashboard_completo(self):
        """Crea un dashboard interactivo completo."""
        print("\n📊 Creando dashboard completo...")
        
        from plotly.subplots import make_subplots
        
        # Dashboard con 6 gráficos
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Tendencia Temporal',
                'Top 10 Productos',
                'Distribución por Categoría',
                'Ventas por Canal',
                'Distribución de Montos',
                'Métricas Clave'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'bar'}],
                [{'type': 'pie'}, {'type': 'bar'}],
                [{'type': 'box'}, {'type': 'table'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Tendencia
        ventas_dia = self.df.groupby('fecha')['total'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=ventas_dia['fecha'], y=ventas_dia['total'], 
                      mode='lines', name='Ingresos', line=dict(color='blue')),
            row=1, col=1
        )
        
        # 2. Top productos
        top_prod = self.df.groupby('producto_nombre')['total'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(y=top_prod['producto_nombre'], x=top_prod['total'], 
                  orientation='h', name='Top Productos'),
            row=1, col=2
        )
        
        # 3. Categorías
        cat_data = self.df.groupby('categoria')['total'].sum()
        fig.add_trace(
            go.Pie(labels=cat_data.index, values=cat_data.values, name='Categorías'),
            row=2, col=1
        )
        
        # 4. Canales
        canal_data = self.df.groupby('canal')['total'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=canal_data['canal'], y=canal_data['total'], name='Canales'),
            row=2, col=2
        )
        
        # 5. Box plot
        fig.add_trace(
            go.Box(y=self.df['total'], name='Distribución'),
            row=3, col=1
        )
        
        # 6. Tabla de métricas
        metricas = pd.DataFrame({
            'Métrica': ['Total Ingresos', 'Total Transacciones', 'Ticket Promedio', 'Productos Vendidos'],
            'Valor': [
                f"€{self.df['total'].sum():,.2f}",
                f"{len(self.df):,}",
                f"€{self.df['total'].mean():.2f}",
                f"{self.df['cantidad'].sum():,}"
            ]
        })
        
        fig.add_trace(
            go.Table(
                header=dict(values=list(metricas.columns), fill_color='paleturquoise'),
                cells=dict(values=[metricas['Métrica'], metricas['Valor']], fill_color='lavender')
            ),
            row=3, col=2
        )
        
        fig.update_layout(
            title_text="Dashboard E-commerce Interactivo",
            height=1200,
            showlegend=False
        )
        
        fig.write_html(self.output_path / '08_dashboard_completo.html')
        print(f"   ✅ Guardado: 08_dashboard_completo.html")
        
        return fig
    
    def ejecutar_todo(self):
        """Ejecuta todas las visualizaciones."""
        print("="*70)
        print("📊 VISUALIZACIONES INTERACTIVAS CON PLOTLY")
        print("="*70)
        
        self.grafico_01_linea_interactiva()
        self.grafico_02_barras_agrupadas()
        self.grafico_03_sunburst()
        self.grafico_04_scatter_3d()
        self.grafico_05_heatmap_calendario()
        self.grafico_06_funnel()
        self.grafico_07_box_violins()
        self.crear_dashboard_completo()
        
        print("\n" + "="*70)
        print("✨ VISUALIZACIONES COMPLETADAS")
        print("="*70)
        print(f"\n📁 8 archivos HTML generados en: {self.output_path}")
        print("\n💡 Abre los archivos .html en tu navegador para interactuar con los gráficos")


def main():
    """Función principal."""
    viz = PlotlyVisualizer()
    viz.ejecutar_todo()


if __name__ == "__main__":
    main()
