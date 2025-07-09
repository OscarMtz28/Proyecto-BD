CREATE INDEX idx_productos_nombre ON Productos(nombre);

CREATE INDEX idx_clientes_nombre_apellido ON Clientes(nombre, apellido);

CREATE INDEX idx_ventas_fecha ON Ventas(fecha_venta);

CREATE INDEX idx_detalle_venta_producto ON Detalle_Venta(id_producto);
CREATE INDEX nombre_indice ON nombre_tabla (columna1, columna2, ...);