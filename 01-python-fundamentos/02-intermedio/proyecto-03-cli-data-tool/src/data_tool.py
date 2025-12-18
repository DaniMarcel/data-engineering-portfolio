"""
CLI Data Tool - Herramienta de Línea de Comandos para Datos
============================================================

Una herramienta CLI profesional para:
- Convertir entre formatos (CSV, JSON, Excel, Parquet)
- Filtrar y transformar datos
- Generar reportes rápidos
- Validar calidad de datos
"""

import click
import pandas as pd
from pathlib import Path
import json

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🔧 Data Tool - Herramienta CLI para manipulación de datos"""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', '-f', type=click.Choice(['csv', 'json', 'excel', 'parquet']),
              help='Formato de salida')
def convert(input_file, output_file, format):
    """Convierte entre formatos de datos.
    
    Ejemplo:
        data-tool convert data.csv data.json -f json
    """
    click.echo(f"📥 Leyendo: {input_file}")
    
    # Detectar formato de entrada
    input_path = Path(input_file)
    if input_path.suffix == '.csv':
        df = pd.read_csv(input_file)
    elif input_path.suffix == '.json':
        df = pd.read_json(input_file)
    elif input_path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(input_file)
    elif input_path.suffix == '.parquet':
        df = pd.read_parquet(input_file)
    else:
        click.echo(f"❌ Formato no soportado: {input_path.suffix}", err=True)
        return
    
    click.echo(f"   ✅ {len(df):,} registros cargados")
    
    # Guardar en formato de salida
    output_path = Path(output_file)
    
    if format == 'csv' or output_path.suffix == '.csv':
        df.to_csv(output_file, index=False)
    elif format == 'json' or output_path.suffix == '.json':
        df.to_json(output_file, orient='records', indent=2)
    elif format == 'excel' or output_path.suffix in ['.xlsx', '.xls']:
        df.to_excel(output_file, index=False)
    elif format == 'parquet' or output_path.suffix == '.parquet':
        df.to_parquet(output_file)
    else:
        click.echo(f"❌ Formato de salida no especificado", err=True)
        return
    
    click.echo(f"💾 Guardado: {output_file}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--rows', '-n', default=10, help='Número de filas a mostrar')
def head(file, rows):
    """Muestra las primeras N filas del archivo.
    
    Ejemplo:
        data-tool head data.csv --rows 20
    """
    df = pd.read_csv(file) if Path(file).suffix == '.csv' else pd.read_json(file)
    
    click.echo(f"\n📊 Primeras {rows} filas de {file}:")
    click.echo("="*80)
    click.echo(df.head(rows).to_string())


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def info(file):
    """Muestra información sobre el dataset.
    
    Ejemplo:
        data-tool info data.csv
    """
    file_path = Path(file)
    
    # Cargar datos
    if file_path.suffix == '.csv':
        df = pd.read_csv(file)
    elif file_path.suffix == '.json':
        df = pd.read_json(file)
    else:
        click.echo(f"❌ Formato no soportado", err=True)
        return
    
    click.echo(f"\n📊 Información de {file}:")
    click.echo("="*80)
    click.echo(f"Filas: {len(df):,}")
    click.echo(f"Columnas: {len(df.columns)}")
    click.echo(f"Tamaño: {file_path.stat().st_size / 1024:.2f} KB")
    click.echo(f"\nColumnas:")
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        click.echo(f"  - {col}: {dtype} ({null_count} nulos)")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', required=True, help='Columna para filtrar')
@click.option('--value', '-v', required=True, help='Valor para filtrar')
@click.option('--output', '-o', type=click.Path(), help='Archivo de salida')
def filter(file, column, value, output):
    """Filtra datos por columna y valor.
    
    Ejemplo:
        data-tool filter data.csv -c ciudad -v Madrid -o madrid.csv
    """
    df = pd.read_csv(file)
    
    click.echo(f"🔍 Filtrando {column} == {value}")
    
    # Intentar conversión numérica
    try:
        value = float(value)
        df_filtered = df[df[column] == value]
    except:
        df_filtered = df[df[column] == value]
    
    click.echo(f"   ✅ {len(df_filtered):,} registros encontrados")
    
    if output:
        df_filtered.to_csv(output, index=False)
        click.echo(f"💾 Guardado: {output}")
    else:
        click.echo(df_filtered.to_string())


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', help='Columna para agrupar')
def stats(file, column):
    """Muestra estadísticas del dataset.
    
    Ejemplo:
        data-tool stats data.csv
        data-tool stats data.csv -c categoria
    """
    df = pd.read_csv(file)
    
    if column:
        click.echo(f"\n📊 Estadísticas agrupadas por '{column}':")
        click.echo("="*80)
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            grouped = df.groupby(column)[numeric_cols].agg(['sum', 'mean', 'count'])
            click.echo(grouped.to_string())
        else:
            click.echo("❌ No hay columnas numéricas para agrupar")
    else:
        click.echo(f"\n📊 Estadísticas descriptivas:")
        click.echo("="*80)
        click.echo(df.describe().to_string())


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def validate(file):
    """Valida calidad de datos.
    
    Ejemplo:
        data-tool validate data.csv
    """
    df = pd.read_csv(file)
    
    click.echo(f"\n✅ Validando calidad de datos en {file}:")
    click.echo("="*80)
    
    # Valores nulos
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        click.echo(f"\n⚠️  Valores nulos encontrados:")
        for col, count in null_counts[null_counts > 0].items():
            pct = (count / len(df)) * 100
            click.echo(f"   - {col}: {count} ({pct:.2f}%)")
    else:
        click.echo("\n✅ No hay valores nulos")
    
    # Duplicados
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        click.echo(f"\n⚠️  {dup_count} filas duplicadas encontradas")
    else:
        click.echo("\n✅ No hay duplicados")
    
    # Tipos de datos
    click.echo(f"\n📊 Tipos de datos:")
    for col, dtype in df.dtypes.items():
        click.echo(f"   - {col}: {dtype}")


@cli.command()
def demo():
    """Ejecuta una demostración de la herramienta."""
    click.echo("\n🎯 DEMO - CLI Data Tool")
    click.echo("="*80)
    click.echo("\n📚 Comandos disponibles:")
    click.echo("  convert  - Convertir entre formatos")
    click.echo("  head     - Ver primeras filas")
    click.echo("  info     - Información del archivo")
    click.echo("  filter   - Filtrar datos")
    click.echo("  stats    - Estadísticas")
    click.echo("  validate - Validar calidad")
    click.echo("\n💡 Usa 'data-tool COMANDO --help' para más información")


if __name__ == '__main__':
    cli()
