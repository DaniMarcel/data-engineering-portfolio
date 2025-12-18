"""Web Analytics Simulation"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulate Google Analytics style data
np.random.seed(42)

dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
data = []

for date in dates:
    sessions = np.random.poisson(500)
    users = int(sessions * 0.7)
    pageviews = int(sessions * 3.2)
    bounce_rate = np.random.uniform(0.35, 0.65)
    avg_duration = np.random.uniform(120, 300)
    
    data.append({
        'date': date,
        'sessions': sessions,
        'users': users,
        'pageviews': pageviews,
        'bounce_rate': bounce_rate,
        'avg_session_duration': avg_duration
    })

df = pd.DataFrame(data)

print("📊 WEB ANALYTICS REPORT\n")
print(f"Period: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"\nOverall Metrics:")
print(f"  Total Sessions: {df['sessions'].sum():,}")
print(f"  Total Users: {df['users'].sum():,}")
print(f"  Total Pageviews: {df['pageviews'].sum():,}")
print(f"  Avg Bounce Rate: {df['bounce_rate'].mean():.2%}")
print(f"  Avg Session Duration: {df['avg_session_duration'].mean():.0f}s")

# Trends
print(f"\nTrends (last 7 days vs previous 7):")
recent = df.tail(7)
previous = df.iloc[-14:-7]
sessions_change = (recent['sessions'].mean() - previous['sessions'].mean()) / previous['sessions'].mean() * 100

print(f"  Sessions: {sessions_change:+.1f}%")

df.to_csv('analytics_report.csv', index=False)
print(f"\n✅ Report saved to analytics_report.csv")
