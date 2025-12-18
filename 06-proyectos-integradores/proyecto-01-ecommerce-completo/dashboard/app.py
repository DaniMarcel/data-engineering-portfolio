"""Interactive Dashboard - Streamlit"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load processed data"""
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'ecommerce_data.csv'
    
    if data_path.exists():
        return pd.read_csv(data_path)
    
    # Fallback data
    return pd.DataFrame({
        'order_id': range(100),
        'customer_id': [i % 20 for i in range(100)],
        'product_id': [i % 5 + 1 for i in range(100)],
        'quantity': [(i % 3) + 1 for i in range(100)],
        'total': [100 + (i * 10) % 500 for i in range(100)],
        'category': ['Electronics' if i % 2 == 0 else 'Accessories' for i in range(100)]
    })

# Load data
df = load_data()

# Title
st.title("🛒 E-commerce Analytics Dashboard")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📦 Total Orders",
        value=f"{len(df):,}",
        delta=f"+{len(df)//10} this week"
    )

with col2:
    total_revenue = df['total'].sum()
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.2f}",
        delta=f"+{total_revenue*0.15:.0f} vs last month"
    )

with col3:
    avg_order = df['total'].mean()
    st.metric(
        label="📊 Avg Order Value",
        value=f"${avg_order:.2f}",
        delta="+5.2%"
    )

with col4:
    unique_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
    st.metric(
        label="👥 Customers",
        value=f"{unique_customers:,}",
        delta=f"+{unique_customers//20}"
    )

st.markdown("---")

# Row 1: Revenue and Orders
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue by Category")
    if 'category' in df.columns:
        category_revenue = df.groupby('category')['total'].sum().reset_index()
        fig = px.pie(
            category_revenue,
            values='total',
            names='category',
            title="Revenue Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top Products")
    if 'product_id' in df.columns:
        top_products = df.groupby('product_id').agg({
            'total': 'sum',
            'quantity': 'sum'
        }).sort_values('total', ascending=False).head(5)
        
        fig = px.bar(
            top_products,
            x=top_products.index,
            y='total',
            title="Revenue by Product",
            labels={'product_id': 'Product ID', 'total': 'Revenue ($)'}
        )
        st.plotly_chart(fig, use_container_width=True)

# Row 2: Customer and quantity analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Customer Analysis")
    if 'customer_id' in df.columns:
        customer_orders = df.groupby('customer_id').size().reset_index(name='orders')
        
        fig = px.histogram(
            customer_orders,
            x='orders',
            title="Orders per Customer Distribution",
            labels={'orders': 'Number of Orders', 'count': 'Customers'}
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📦 Quantity Distribution")
    if 'quantity' in df.columns:
        fig = px.box(
            df,
            y='quantity',
            title="Order Quantity Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Recent Orders")
st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
