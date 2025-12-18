"""
Lector y Analizador de Archivos CSV
====================================

Este script demuestra cómo trabajar con archivos CSV en Python usando solo
la biblioteca estándar (sin pandas).

Objetivos de aprendizaje:
- Lectura de archivos CSV
- Manejo de excepciones
- Validación de datos
- Estadísticas básicas
- Formateo de salida
"""

import csv
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class AnalizadorVentas:
    """Clase para analizar datos de ventas desde archivos CSV."""
    
    def __init__(self, archivo_csv):
        """
        Inicializa el analizador con la ruta del archivo CSV.
        
        Args:
            archivo_csv (str): Ruta al archivo CSV con datos de ventas
        """
        self.archivo = Path(archivo_csv)
        self.ventas = []
        self.errores = []
    
    def leer_csv(self):
        """Lee el archivo CSV y carga los datos en memoria."""
        print(f"📂 Leyendo archivo: {self.archivo.name}")
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, start=2):  # start=2 porque línea 1 es header
                    try:
                        # Validar y convertir datos
                        venta = self._validar_fila(row, i)
                        if venta:
                            self.ventas.append(venta)
                    except Exception as e:
                        self.errores.append(f"Línea {i}: {str(e)}")
            
            print(f"✅ Registros válidos leídos: {len(self.ventas)}")
            if self.errores:
                print(f"⚠️  Registros con errores: {len(self.errores)}")
            
        except FileNotFoundError:
            print(f"❌ Error: El archivo '{self.archivo}' no existe")
            return False
        except Exception as e:
            print(f"❌ Error al leer el archivo: {str(e)}")
            return False
        
        return True
    
    def _validar_fila(self, row, num_linea):
        """
        Valida y convierte los datos de una fila.
        
        Args:
            row (dict): Fila del CSV como diccionario
            num_linea (int): Número de línea para mensajes de error
            
        Returns:
            dict: Datos validados o None si hay errores
        """
        try:
            # Convertir cantidad a entero
            cantidad = row['cantidad']
            if not cantidad or cantidad == '':
                raise ValueError(f"Cantidad vacía")
            cantidad = int(cantidad)
            
            # Convertir total a float
            total = row['total']
            if total == 'ERROR' or not total:
                raise ValueError(f"Total inválido: {total}")
            total = float(total)
            
            # Validar fecha
            fecha = datetime.strptime(row['fecha'], '%Y-%m-%d')
            
            return {
                'id_venta': int(row['id_venta']),
                'fecha': row['fecha'],
                'producto': row['producto'],
                'categoria': row['categoria'],
                'cantidad': cantidad,
                'precio_unitario': float(row['precio_unitario']),
                'total': total,
                'ciudad': row['ciudad'],
                'metodo_pago': row['metodo_pago'],
            }
        except Exception as e:
            raise ValueError(f"{str(e)}")
    
    def resumen_general(self):
        """Muestra estadísticas generales de las ventas."""
        if not self.ventas:
            print("❌ No hay datos para analizar")
            return
        
        total_ventas = sum(v['total'] for v in self.ventas)
        total_productos = sum(v['cantidad'] for v in self.ventas)
        promedio_venta = total_ventas / len(self.ventas)
        
        print("\n" + "="*60)
        print("📊 RESUMEN GENERAL DE VENTAS")
        print("="*60)
        print(f"Total de transacciones: {len(self.ventas):,}")
        print(f"Total de productos vendidos: {total_productos:,}")
        print(f"Ingresos totales: €{total_ventas:,.2f}")
        print(f"Promedio por venta: €{promedio_venta:,.2f}")
        print(f"Venta mínima: €{min(v['total'] for v in self.ventas):,.2f}")
        print(f"Venta máxima: €{max(v['total'] for v in self.ventas):,.2f}")
    
    def ventas_por_categoria(self):
        """Analiza ventas agrupadas por categoría."""
        ventas_cat = defaultdict(lambda: {'total': 0, 'cantidad': 0})
        
        for venta in self.ventas:
            cat = venta['categoria']
            ventas_cat[cat]['total'] += venta['total']
            ventas_cat[cat]['cantidad'] += venta['cantidad']
        
        print("\n" + "="*60)
        print("📦 VENTAS POR CATEGORÍA")
        print("="*60)
        
        # Ordenar por total de ventas (descendente)
        categorias_ordenadas = sorted(
            ventas_cat.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )
        
        for categoria, datos in categorias_ordenadas:
            print(f"\n{categoria}:")
            print(f"  💰 Ingresos: €{datos['total']:,.2f}")
            print(f"  📦 Unidades vendidas: {datos['cantidad']:,}")
    
    def ventas_por_ciudad(self):
        """Analiza ventas agrupadas por ciudad."""
        ventas_ciudad = defaultdict(float)
        
        for venta in self.ventas:
            ventas_ciudad[venta['ciudad']] += venta['total']
        
        print("\n" + "="*60)
        print("🌍 VENTAS POR CIUDAD")
        print("="*60)
        
        ciudades_ordenadas = sorted(
            ventas_ciudad.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for i, (ciudad, total) in enumerate(ciudades_ordenadas, 1):
            print(f"{i}. {ciudad}: €{total:,.2f}")
    
    def top_productos(self, n=5):
        """Muestra los productos más vendidos."""
        productos_vendidos = defaultdict(lambda: {'cantidad': 0, 'ingresos': 0})
        
        for venta in self.ventas:
            prod = venta['producto']
            productos_vendidos[prod]['cantidad'] += venta['cantidad']
            productos_vendidos[prod]['ingresos'] += venta['total']
        
        print(f"\n" + "="*60)
        print(f"🏆 TOP {n} PRODUCTOS MÁS VENDIDOS")
        print("="*60)
        
        # Ordenar por cantidad vendida
        top = sorted(
            productos_vendidos.items(),
            key=lambda x: x[1]['cantidad'],
            reverse=True
        )[:n]
        
        for i, (producto, datos) in enumerate(top, 1):
            print(f"\n{i}. {producto}")
            print(f"   Unidades: {datos['cantidad']:,}")
            print(f"   Ingresos: €{datos['ingresos']:,.2f}")
    
    def metodos_pago(self):
        """Analiza la distribución de métodos de pago."""
        metodos = Counter(v['metodo_pago'] for v in self.ventas)
        
        print("\n" + "="*60)
        print("💳 MÉTODOS DE PAGO")
        print("="*60)
        
        for metodo, cantidad in metodos.most_common():
            porcentaje = (cantidad / len(self.ventas)) * 100
            print(f"{metodo}: {cantidad:,} ({porcentaje:.1f}%)")
    
    def guardar_errores(self, archivo_salida):
        """Guarda los errores encontrados en un archivo."""
        if not self.errores:
            return
        
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("ERRORES ENCONTRADOS EN LA VALIDACIÓN\n")
            f.write("="*60 + "\n\n")
            for error in self.errores:
                f.write(f"- {error}\n")
        
        print(f"\n📝 Errores guardados en: {archivo}")
    
    def generar_reporte_completo(self):
        """Genera un reporte completo con todos los análisis."""
        self.resumen_general()
        self.ventas_por_categoria()
        self.ventas_por_ciudad()
        self.top_productos(5)
        self.metodos_pago()


def main():
    """Función principal del programa."""
    print("="*60)
    print("🔍 ANALIZADOR DE VENTAS CSV")
    print("="*60 + "\n")
    
    # Rutas de archivos
    archivo_datos = Path(__file__).parent.parent / "data" / "raw" / "ventas_2024.csv"
    archivo_errores = Path(__file__).parent.parent / "output" / "errores_validacion.txt"
    
    # Crear analizador
    analizador = AnalizadorVentas(archivo_datos)
    
    # Leer y procesar datos
    if analizador.leer_csv():
        analizador.generar_reporte_completo()
        
        # Guardar errores si los hay
        if analizador.errores:
            analizador.guardar_errores(archivo_errores)
    
    print("\n" + "="*60)
    print("✨ Análisis completado")
    print("="*60)


if __name__ == "__main__":
    main()
