-- =====================================================
-- DATOS DE EJEMPLO - E-COMMERCE
-- =====================================================

-- Insertar categorías
INSERT INTO categorias (nombre, descripcion) VALUES
('Electrónica', 'Dispositivos y gadgets electrónicos'),
('Hogar', 'Artículos para el hogar'),
('Deporte', 'Equipamiento deportivo'),
('Libros', 'Libros y publicaciones'),
('Belleza', 'Productos de belleza y cuidado personal'),
('Alimentación', 'Productos alimenticios');

-- Insertar usuarios
INSERT INTO usuarios (email, nombre, apellido, password_hash, tipo_usuario) VALUES
('admin@ecommerce.com', 'Admin', 'Sistema', '$2y$10$hash', 'admin'),
('juan.perez@email.com', 'Juan', 'Pérez', '$2y$10$hash', 'cliente'),
('maria.garcia@email.com', 'María', 'García', '$2y$10$hash', 'cliente'),
('carlos.lopez@email.com', 'Carlos', 'López', '$2y$10$hash', 'cliente');

-- Insertar direcciones
INSERT INTO direcciones (usuario_id, alias, calle, ciudad, codigo_postal) VALUES
(2, 'Casa', 'Calle Mayor 123', 'Madrid', '28001'),
(3, 'Oficina', 'Av. Diagonal 456', 'Barcelona', '08001'),
(4, 'Casa', 'Gran Vía 789', 'Valencia', '46001');

-- Insertar productos
INSERT INTO productos (sku, nombre, categoria_id, precio_base, costo, stock_actual) VALUES
('ELEC-LAP-001', 'Laptop Dell XPS 13', 1, 1299.99, 800.00, 15),
('ELEC-MOU-001', 'Mouse Logitech MX', 1, 99.99, 50.00, 50),
('HOME-SIL-001', 'Silla Ergonómica', 2, 299.99, 150.00, 20),
('DEPO-BIC-001', 'Bicicleta Mountain', 3, 599.99, 350.00, 10),
('LIBR-NOV-001', 'Novela Bestseller', 4, 19.99, 8.00, 100);

-- Ver el esquema creado
SELECT 'Schema creado exitosamente' as mensaje;
