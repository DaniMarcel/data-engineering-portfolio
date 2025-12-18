"""
Validación de Datos con Pydantic
=================================

Pydantic permite validar datos con:
- Type hints y validación automática
- Modelos reutilizables
- Mensajes de error claros
- Serialización/deserialización
- Validadores personalizados
"""

from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import List, Optional, Literal
from datetime import datetime, date
from decimal import Decimal
import json

# ============= MODELOS BÁSICOS =============

class Usuario(BaseModel):
    """Modelo de usuario con validaciones."""
    
    usuario_id: int = Field(..., gt=0, description="ID único del usuario")
    email: EmailStr = Field(..., description="Email válido")
    nombre: str = Field(..., min_length=2, max_length=100)
    edad: int = Field(..., ge=18, le=120, description="Edad entre 18 y 120")
    activo: bool = True
    fecha_registro: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario_id": 1,
                "email": "usuario@example.com",
                "nombre": "Juan Pérez",
                "edad": 30,
                "activo": True
            }
        }


class Direccion(BaseModel):
    """Modelo de dirección."""
    
    calle: str = Field(..., min_length=5)
    ciudad: str = Field(..., min_length=2)
    codigo_postal: str = Field(..., regex=r'^\d{5}$')
    pais: str = "España"


class Producto(BaseModel):
    """Modelo de producto con validadores personalizados."""
    
    producto_id: int = Field(..., gt=0)
    sku: str = Field(..., regex=r'^[A-Z]{3}-[A-Z]{3}-\d{3}$')
    nombre: str = Field(..., min_length=3, max_length=200)
    precio: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    categoria: Literal['Electrónica', 'Hogar', 'Deporte', 'Libros', 'Belleza']
    peso_kg: Optional[float] = Field(None, gt=0)
    activo: bool = True
    
    @validator('nombre')
    def nombre_debe_ser_capitalizado(cls, v):
        """Valida que el nombre esté capitalizado."""
        if not v[0].isupper():
            raise ValueError('El nombre debe comenzar con mayúscula')
        return v
    
    @validator('precio')
    def precio_razonable(cls, v):
        """Valida que el precio sea razonable."""
        if v > 10000:
            raise ValueError('Precio parece demasiado alto, verifica')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "producto_id": 1,
                "sku": "ELE-LAP-001",
                "nombre": "Laptop Dell",
                "precio": "1299.99",
                "stock": 10,
                "categoria": "Electrónica"
            }
        }


class Transaccion(BaseModel):
    """Modelo de transacción e-commerce."""
    
    transaccion_id: int
    usuario_id: int
    fecha: date
    productos: List[int] = Field(..., min_items=1, max_items=50)
    subtotal: Decimal = Field(..., gt=0)
    descuento: Decimal = Field(default=Decimal('0'), ge=0)
    total: Decimal = Field(..., gt=0)
    metodo_pago: Literal['tarjeta', 'paypal', 'transferencia']
    estado: Literal['pendiente', 'completado', 'cancelado'] = 'pendiente'
    
    @root_validator
    def validar_total(cls, values):
        """Valida que el total sea correcto."""
        subtotal = values.get('subtotal')
        descuento = values.get('descuento')
        total = values.get('total')
        
        if all([subtotal, descuento, total]):
            total_calculado = subtotal - descuento
            if abs(total - total_calculado) > Decimal('0.01'):
                raise ValueError(
                    f'Total incorrecto: esperado {total_calculado}, recibido {total}'
                )
        
        return values
    
    @validator('descuento')
    def descuento_no_mayor_que_subtotal(cls, v, values):
        """Valida que el descuento no sea mayor que el subtotal."""
        if 'subtotal' in values and v > values['subtotal']:
            raise ValueError('El descuento no puede ser mayor que el subtotal')
        return v


# ============= VALIDADOR DE DATOS =============

class DataValidator:
    """Clase para validar datos con Pydantic."""
    
    def __init__(self):
        self.errores = []
        self.validos = []
    
    def validar_usuarios(self, datos: List[dict]) -> tuple:
        """Valida lista de usuarios."""
        print(f"\n👥 Validando {len(datos)} usuarios...")
        
        for i, dato in enumerate(datos):
            try:
                usuario = Usuario(**dato)
                self.validos.append(usuario)
            except Exception as e:
                self.errores.append({
                    'index': i,
                    'data': dato,
                    'error': str(e)
                })
        
        print(f"   ✅ Válidos: {len(self.validos)}")
        print(f"   ❌ Errores: {len(self.errores)}")
        
        return self.validos, self.errores
    
    def validar_productos(self, datos: List[dict]) -> tuple:
        """Valida lista de productos."""
        print(f"\n📦 Validando {len(datos)} productos...")
        
        self.errores = []
        self.validos = []
        
        for i, dato in enumerate(datos):
            try:
                producto = Producto(**dato)
                self.validos.append(producto)
            except Exception as e:
                self.errores.append({
                    'index': i,
                    'data': dato,
                    'error': str(e)
                })
        
        print(f"   ✅ Válidos: {len(self.validos)}")
        print(f"   ❌ Errores: {len(self.errores)}")
        
        return self.validos, self.errores
    
    def mostrar_errores(self):
        """Muestra detalles de errores."""
        if not self.errores:
            print("\n✅ No hay errores")
            return
        
        print(f"\n❌ Detalles de {len(self.errores)} errores:")
        print("="*80)
        
        for error in self.errores[:10]:  # Mostrar primeros 10
            print(f"\nRegistro #{error['index']}:")
            print(f"  Datos: {error['data']}")
            print(f"  Error: {error['error']}")


# ============= EJEMPLOS =============

def ejemplo_validacion_basica():
    """Ejemplo básico de validación."""
    print("\n" + "="*80)
    print("📝 EJEMPLO: VALIDACIÓN BÁSICA")
    print("="*80)
    
    # Válido
    try:
        usuario1 = Usuario(
            usuario_id=1,
            email="juan@example.com",
            nombre="Juan Pérez",
            edad=30
        )
        print(f"\n✅ Usuario válido: {usuario1.email}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Inválido - email mal formado
    try:
        usuario2 = Usuario(
            usuario_id=2,
            email="email-invalido",
            nombre="Ana",
            edad=25
        )
    except Exception as e:
        print(f"\n❌ Error esperado (email inválido): {e}")
    
    # Inválido - edad fuera de rango
    try:
        usuario3 = Usuario(
            usuario_id=3,
            email="carlos@example.com",
            nombre="Carlos",
            edad=15  # Menor de 18
        )
    except Exception as e:
        print(f"\n❌ Error esperado (edad < 18): {e}")


def ejemplo_validacion_producto():
    """Ejemplo de validación de producto."""
    print("\n" + "="*80)
    print("📦 EJEMPLO: VALIDACIÓN DE PRODUCTO")
    print("="*80)
    
    # Válido
    try:
        producto1 = Producto(
            producto_id=1,
            sku="ELE-LAP-001",
            nombre="Laptop Dell",
            precio=Decimal("1299.99"),
            stock=10,
            categoria="Electrónica"
        )
        print(f"\n✅ Producto válido: {producto1.nombre}")
        print(f"   SKU: {producto1.sku}")
        print(f"   Precio: €{producto1.precio}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Inválido - SKU mal formato
    try:
        producto2 = Producto(
            producto_id=2,
            sku="INVALID-SKU",
            nombre="Mouse",
            precio=Decimal("29.99"),
            stock=50,
            categoria="Electrónica"
        )
    except Exception as e:
        print(f"\n❌ Error esperado (SKU inválido): {e}")


def ejemplo_validacion_transaccion():
    """Ejemplo de validación de transacción."""
    print("\n" + "="*80)
    print("💳 EJEMPLO: VALIDACIÓN DE TRANSACCIÓN")
    print("="*80)
    
    # Válido
    try:
        trans1 = Transaccion(
            transaccion_id=1,
            usuario_id=1,
            fecha=date.today(),
            productos=[1, 2, 3],
            subtotal=Decimal("100.00"),
            descuento=Decimal("10.00"),
            total=Decimal("90.00"),
            metodo_pago="tarjeta"
        )
        print(f"\n✅ Transacción válida:")
        print(f"   Subtotal: €{trans1.subtotal}")
        print(f"   Descuento: €{trans1.descuento}")
        print(f"   Total: €{trans1.total}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Inválido - total incorrecto
    try:
        trans2 = Transaccion(
            transaccion_id=2,
            usuario_id=1,
            fecha=date.today(),
            productos=[1],
            subtotal=Decimal("100.00"),
            descuento=Decimal("10.00"),
            total=Decimal("100.00"),  # Debería ser 90
            metodo_pago="paypal"
        )
    except Exception as e:
        print(f"\n❌ Error esperado (total incorrecto): {e}")


def ejemplo_validacion_lote():
    """Ejemplo de validación en lote."""
    print("\n" + "="*80)
    print("📊 EJEMPLO: VALIDACIÓN EN LOTE")
    print("="*80)
    
    # Datos de ejemplo (algunos válidos, algunos no)
    usuarios_data = [
        {"usuario_id": 1, "email": "juan@example.com", "nombre": "Juan", "edad": 30},
        {"usuario_id": 2, "email": "invalido", "nombre": "Ana", "edad": 25},
        {"usuario_id": 3, "email": "carlos@example.com", "nombre": "C", "edad": 28},
        {"usuario_id": 4, "email": "maria@example.com", "nombre": "María", "edad": 150},
        {"usuario_id": 5, "email": "luis@example.com", "nombre": "Luis", "edad": 35},
    ]
    
    validator = DataValidator()
    validos, errores = validator.validar_usuarios(usuarios_data)
    
    validator.mostrar_errores()
    
    # Exportar válidos
    if validos:
        print(f"\n💾 Exportando {len(validos)} usuarios válidos...")
        usuarios_json = [u.model_dump() for u in validos]
        print(f"   Ejemplo: {usuarios_json[0]}")


def main():
    """Función principal."""
    print("="*80)
    print("✅ VALIDACIÓN DE DATOS CON PYDANTIC")
    print("="*80)
    
    ejemplo_validacion_basica()
    ejemplo_validacion_producto()
    ejemplo_validacion_transaccion()
    ejemplo_validacion_lote()
    
    print("\n" + "="*80)
    print("✨ EJEMPLOS COMPLETADOS")
    print("="*80)
    print("\n💡 Pydantic te permite:")
    print("   - Validar tipos automáticamente")
    print("   - Definir reglas de validación complejas")
    print("   - Mensajes de error claros")
    print("   - Serialización JSON fácil")


if __name__ == "__main__":
    main()
