"""Statistical Hypothesis Testing"""
from scipy import stats
import numpy as np
import pandas as pd
from pathlib import Path

# Load data
# Buscar carpeta base \'data engineer\'

current_path = Path(__file__).resolve()

base_path = None

for parent in current_path.parents:

    if parent.name == \'data engineer\':

        base_path = parent

        break

if base_path is None:

    raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
df = pd.read_csv(base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv')

print("📊 STATISTICAL HYPOTHESIS TESTING\n")

# 1. T-test: Compare average sales between two categories
cat1 = df[df['categoria'] == 'Electrónica']['total']
cat2 = df[df['categoria'] == 'Hogar']['total']

t_stat, p_value = stats.ttest_ind(cat1, cat2)
print(f"1. T-Test: Electrónica vs Hogar")
print(f"   T-statistic: {t_stat:.4f}")
print(f"   P-value: {p_value:.4f}")
print(f"   Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")

# 2. Chi-square test: Category distribution
observed = df['categoria'].value_counts()
expected = np.array([len(df) / len(observed)] * len(observed))
chi2, p_value = stats.chisquare(observed, expected)
print(f"\n2. Chi-Square Test: Category distribution")
print(f"   Chi-square: {chi2:.4f}")
print(f"   P-value: {p_value:.4f}")

# 3. Normality test
_, p_value = stats.normaltest(df['total'])
print(f"\n3. Normality Test (total sales)")
print(f"   P-value: {p_value:.4f}")
print(f"   Distribution: {'Normal' if p_value > 0.05 else 'Not normal'}")

# 4. Correlation test
corr, p_value = stats.pearsonr(df['cantidad'], df['total'])
print(f"\n4. Correlation: cantidad vs total")
print(f"   Pearson r: {corr:.4f}")
print(f"   P-value: {p_value:.4f}")

print("\n✅ Analysis completed!")
