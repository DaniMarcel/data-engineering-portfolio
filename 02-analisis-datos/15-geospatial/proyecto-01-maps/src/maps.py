"""Geospatial Analysis with Folium"""
import folium
import pandas as pd

# Spanish cities with sales data
cities = {
    'city': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'],
    'lat': [40.4168, 41.3851, 39.4699, 37.3891, 43.2630],
    'lon': [-3.7038, 2.1734, -0.3763, -5.9845, -2.9350],
    'sales': [150000, 120000, 80000, 75000, 60000]
}

df = pd.DataFrame(cities)

# Create map
m = folium.Map(location=[40.0, -4.0], zoom_start=6)

# Add markers
for _, row in df.iterrows():
    folium.CircleMarker(
        [row['lat'], row['lon']],
        radius=row['sales']/10000,
        popup=f"{row['city']}: €{row['sales']:,}",
        color='red',
        fill=True
    ).add_to(m)

m.save('sales_map.html')
print("✅ Map saved to sales_map.html")
