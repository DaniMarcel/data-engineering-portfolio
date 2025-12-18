"""Pandas Performance Optimization - Extended"""
import pandas as pd
import numpy as np
from pathlib import Path
import time

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

print("⚡ PANDAS PERFORMANCE OPTIMIZATION\n")

# 1. Use .query() vs boolean indexing
print("1. Query vs Boolean Indexing:")
start = time.time()
result1 = df[df['total'] > 100]
bool_time = time.time() - start

start = time.time()
result2 = df.query('total > 100')
query_time = time.time() - start

print(f"   Boolean: {bool_time:.4f}s")
print(f"   Query: {query_time:.4f}s")
print(f"   Speedup: {bool_time/query_time:.2f}x")

# 2. Category dtype for memory
print("\n2. Memory Optimization (Category dtype):")
mem_before = df.memory_usage(deep=True).sum() / 1024**2
df_opt = df.copy()
df_opt['categoria'] = df_opt['categoria'].astype('category')
df_opt['ciudad_envio'] = df_opt['ciudad_envio'].astype('category')
mem_after = df_opt.memory_usage(deep=True).sum() / 1024**2

print(f"   Before: {mem_before:.2f} MB")
print(f"   After: {mem_after:.2f} MB")  
print(f"   Reduction: {(1 - mem_after/mem_before)*100:.1f}%")

# 3. Vectorization
print("\n3. Vectorization:")
print(f"   Always use vectorized operations")
print(f"   df['new_col'] = df['a'] * df['b']  ✅")
print(f"   df.apply(lambda x: x['a'] * x['b'])  ❌ (slower)")

print("\n✅ Optimization examples completed!")
