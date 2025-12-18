# 🗄️ Schema E-commerce MySQL

## 🎯 Objetivos

- ✅ Diseño completo de base de datos e-commerce
- ✅ Normalización hasta 3NF
- ✅ Relaciones y claves foráneas
- ✅ Vistas útiles
- ✅ Procedimientos almacenados
- ✅ Índices optimizados

## 📊 Tablas Incluidas

1. **usuarios** - Gestión de usuarios
2. **direcciones** - Direcciones de envío
3. **categorias** - Categorías de productos (jerárquicas)
4. **productos** - Catálago de productos
5. **ordenes** - Órdenes de compra
6. **orden_detalles** - Items de cada orden
7. **reviews** - Reseñas de productos
8. **carrito** - Carrito de compras activo
9. **inventario_movimientos** - Auditoría de inventario

## 🚀 Uso

### 1. Crear la base de datos

```sql
CREATE DATABASE ecommerce;
USE ecommerce;
```

### 2. Ejecutar el schema

```bash
mysql -u root -p ecommerce < sql/01_create_schema.sql
```

### 3. Insertar datos de ejemplo

```bash
mysql -u root -p ecommerce < sql/02_insert_data.sql
```

## 💡 Características

- **Vistas**: productos_stock_bajo, usuario_ordenes_resumen, top_productos_vendidos
- **Procedimiento**: crear_orden() - Crea orden desde carrito automáticamente
- **Índices**: Optimizados para queries comunes
- **Constraints**: Integridad referencial completa

## 📝 Queries de Ejemplo

Ver `sql/03_queries_ejemplo.sql`

---

Este schema es production-ready y sigue mejores prácticas de diseño de BD.
