"""Dash Interactive Dashboard - Extended"""
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

app = dash.Dash(__name__)

# Load data - buscar carpeta base
current_path = Path(__file__).resolve()
base = None
for parent in current_path.parents:
    if parent.name == 'data engineer':
        base = parent
        break
if base is None:
    raise FileNotFoundError("No se pudo encontrar la carpeta base 'data engineer'")

df = pd.read_csv(base / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

# Layout
app.layout = html.Div([
    html.H1("📊 Interactive Sales Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div([
        html.Label('Select Category:'),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in sorted(df['categoria'].unique())],
            value=df['categoria'].unique()[0],
            style={'width': '300px'}
        ),
    ], style={'padding': '20px'}),
    
    html.Div([
        html.Div([dcc.Graph(id='sales-over-time')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='top-products')], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ]),
    
    html.Div([
        html.Div([dcc.Graph(id='sales-distribution')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='city-breakdown')], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ]),
])

@callback(
    [Output('sales-over-time', 'figure'),
     Output('top-products', 'figure'),
     Output('sales-distribution', 'figure'),
     Output('city-breakdown', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_graphs(selected_category):
    filtered_df = df[df['categoria'] == selected_category]
    
    # Time series
    daily_sales = filtered_df.groupby('fecha')['total'].sum().reset_index()
    fig1 = px.line(daily_sales, x='fecha', y='total', title=f'Sales Over Time - {selected_category}')
    
    # Top products
    top_products = filtered_df.groupby('producto_nombre')['total'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_products, x='total', y='producto_nombre', orientation='h',
                  title='Top 10 Products')
    
    # Distribution
    fig3 = px.histogram(filtered_df, x='total', nbins=50, title='Sales Distribution')
    
    # By city
    city_sales = filtered_df.groupby('ciudad_envio')['total'].sum().nlargest(10).reset_index()
    fig4 = px.pie(city_sales, values='total', names='ciudad_envio', title='Sales by City')
    
    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    print("🚀 Starting Dash app on http://localhost:8050")
    app.run(debug=True, port=8050)
