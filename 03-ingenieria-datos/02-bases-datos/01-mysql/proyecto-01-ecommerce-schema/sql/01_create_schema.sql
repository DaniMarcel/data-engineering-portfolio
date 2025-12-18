-- =====================================================
-- SCHEMA E-COMMERCE - MySQL
-- =====================================================
-- Este schema demuestra diseño de base de datos para e-commerce
-- Incluye: usuarios, productos, órdenes, inventario, reviews

-- =====================================================
-- 1. TABLA USUARIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME,
    activo BOOLEAN DEFAULT TRUE,
    tipo_usuario ENUM('cliente', 'admin', 'vendedor') DEFAULT 'cliente',
    INDEX idx_email (email),
    INDEX idx_fecha_registro (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 2. TABLA DIRECCIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS direcciones (
    direccion_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    alias VARCHAR(50) DEFAULT 'Casa',
    calle VARCHAR(255) NOT NULL,
    numero VARCHAR(20),
    ciudad VARCHAR(100) NOT NULL,
    provincia VARCHAR(100),
    codigo_postal VARCHAR(20),
    pais VARCHAR(100) DEFAULT 'España',
    es_principal BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 3. TABLA CATEGORÍAS
-- =====================================================
CREATE TABLE IF NOT EXISTS categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    categoria_padre_id INT,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (categoria_padre_id) REFERENCES categorias(categoria_id) ON DELETE SET NULL,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 4. TABLA PRODUCTOS
-- =====================================================
CREATE TABLE IF NOT EXISTS productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    precio_base DECIMAL(10, 2) NOT NULL,
    precio_oferta DECIMAL(10, 2),
    costo DECIMAL(10, 2),
    peso_kg DECIMAL(8, 2),
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 5,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE SET NULL,
    INDEX idx_sku (sku),
    INDEX idx_categoria (categoria_id),
    INDEX idx_precio (precio_base)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 5. TABLA ÓRDENES
-- =====================================================
CREATE TABLE IF NOT EXISTS ordenes (
    orden_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    direccion_envio_id INT NOT NULL,
    numero_orden VARCHAR(50) UNIQUE NOT NULL,
    fecha_orden DATETIME DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(10, 2) DEFAULT 0,
    impuestos DECIMAL(10, 2) DEFAULT 0,
    gastos_envio DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    estado ENUM('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
    metodo_pago ENUM('tarjeta', 'paypal', 'transferencia', 'contra_reembolso') NOT NULL,
    fecha_envio DATETIME,
    fecha_entrega DATETIME,
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (direccion_envio_id) REFERENCES direcciones(direccion_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha_orden (fecha_orden),
    INDEX idx_estado (estado),
    INDEX idx_numero_orden (numero_orden)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 6. TABLA DETALLES ORDEN
-- =====================================================
CREATE TABLE IF NOT EXISTS orden_detalles (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    orden_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    descuento_unitario DECIMAL(10, 2) DEFAULT 0,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (orden_id) REFERENCES ordenes(orden_id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id),
    INDEX idx_orden (orden_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 7. TABLA REVIEWS
-- =====================================================
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    producto_id INT NOT NULL,
    usuario_id INT NOT NULL,
    orden_id INT,
    calificacion INT CHECK (calificacion BETWEEN 1 AND 5),
    titulo VARCHAR(255),
    comentario TEXT,
    fecha_review DATETIME DEFAULT CURRENT_TIMESTAMP,
    verificado BOOLEAN DEFAULT FALSE,
    util_count INT DEFAULT 0,
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (orden_id) REFERENCES ordenes(orden_id) ON DELETE SET NULL,
    INDEX idx_producto (producto_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_calificacion (calificacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 8. TABLA CARRITO (para sesiones activas)
-- =====================================================
CREATE TABLE IF NOT EXISTS carrito (
    carrito_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario_producto (usuario_id, producto_id),
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 9. TABLA MOVIMIENTOS INVENTARIO
-- =====================================================
CREATE TABLE IF NOT EXISTS inventario_movimientos (
    movimiento_id INT PRIMARY KEY AUTO_INCREMENT,
    producto_id INT NOT NULL,
    tipo_movimiento ENUM('entrada', 'salida', 'ajuste') NOT NULL,
    cantidad INT NOT NULL,
    stock_anterior INT NOT NULL,
    stock_nuevo INT NOT NULL,
    motivo VARCHAR(255),
    usuario_responsable_id INT,
    fecha_movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id),
    FOREIGN KEY (usuario_responsable_id) REFERENCES usuarios(usuario_id),
    INDEX idx_producto (producto_id),
    INDEX idx_fecha (fecha_movimiento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista: Productos con stock bajo
CREATE OR REPLACE VIEW productos_stock_bajo AS
SELECT 
    p.producto_id,
    p.sku,
    p.nombre,
    p.stock_actual,
    p.stock_minimo,
    c.nombre as categoria
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE p.stock_actual <= p.stock_minimo AND p.activo = TRUE;

-- Vista: Resumen de órdenes por usuario
CREATE OR REPLACE VIEW usuario_ordenes_resumen AS
SELECT 
    u.usuario_id,
    u.email,
    u.nombre,
    COUNT(o.orden_id) as total_ordenes,
    SUM(o.total) as total_gastado,
    AVG(o.total) as promedio_orden,
    MAX(o.fecha_orden) as ultima_orden
FROM usuarios u
LEFT JOIN ordenes o ON u.usuario_id = o.usuario_id
GROUP BY u.usuario_id, u.email, u.nombre;

-- Vista: Top productos más vendidos
CREATE OR REPLACE VIEW top_productos_vendidos AS
SELECT 
    p.producto_id,
    p.nombre,
    p.sku,
    COUNT(od.detalle_id) as num_ventas,
    SUM(od.cantidad) as unidades_vendidas,
    SUM(od.subtotal) as ingresos_totales
FROM productos p
INNER JOIN orden_detalles od ON p.producto_id = od.producto_id
INNER JOIN ordenes o ON od.orden_id = o.orden_id
WHERE o.estado != 'cancelado'
GROUP BY p.producto_id, p.nombre, p.sku
ORDER BY ingresos_totales DESC;

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- =====================================================

DELIMITER //

-- Procedimiento: Crear nueva orden
CREATE PROCEDURE crear_orden(
    IN p_usuario_id INT,
    IN p_direccion_id INT,
    IN p_metodo_pago VARCHAR(20)
)
BEGIN
    DECLARE v_orden_id INT;
    DECLARE v_numero_orden VARCHAR(50);
    DECLARE v_subtotal DECIMAL(10,2);
    
    -- Generar número de orden único
    SET v_numero_orden = CONCAT('ORD-', LPAD(FLOOR(RAND() * 999999), 6, '0'));
    
    -- Calcular subtotal del carrito
    SELECT SUM(p.precio_base * c.cantidad)
    INTO v_subtotal
    FROM carrito c
    JOIN productos p ON c.producto_id = p.producto_id
    WHERE c.usuario_id = p_usuario_id;
    
    -- Crear orden
    INSERT INTO ordenes (usuario_id, direccion_envio_id, numero_orden, subtotal, total, metodo_pago)
    VALUES (p_usuario_id, p_direccion_id, v_numero_orden, v_subtotal, v_subtotal, p_metodo_pago);
    
    SET v_orden_id = LAST_INSERT_ID();
    
    -- Copiar items del carrito a orden_detalles
    INSERT INTO orden_detalles (orden_id, producto_id, cantidad, precio_unitario, subtotal)
    SELECT 
        v_orden_id,
        c.producto_id,
        c.cantidad,
        p.precio_base,
        p.precio_base * c.cantidad
    FROM carrito c
    JOIN productos p ON c.producto_id = p.producto_id
    WHERE c.usuario_id = p_usuario_id;
    
    -- Actualizar inventario
    UPDATE productos p
    INNER JOIN carrito c ON p.producto_id = c.producto_id
    SET p.stock_actual = p.stock_actual - c.cantidad
    WHERE c.usuario_id = p_usuario_id;
    
    -- Limpiar carrito
    DELETE FROM carrito WHERE usuario_id = p_usuario_id;
    
    SELECT v_orden_id as orden_id, v_numero_orden as numero_orden;
END //

DELIMITER ;

-- =====================================================
-- INDICES ADICIONALES PARA RENDIMIENTO
-- =====================================================

CREATE INDEX idx_ordenes_fecha_estado ON ordenes(fecha_orden, estado);
CREATE INDEX idx_productos_activo_precio ON productos(activo, precio_base);
CREATE INDEX idx_reviews_producto_calificacion ON reviews(producto_id, calificacion);
