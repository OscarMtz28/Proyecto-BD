CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50),
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT TRUE
);
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    puntos_fidelidad INT DEFAULT 0
);
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(12,2) NOT NULL,
    metodo_pago VARCHAR(50),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);
CREATE TABLE Detalle_Venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(12,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ubicacion VARCHAR(50),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);