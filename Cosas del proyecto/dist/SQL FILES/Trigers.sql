CREATE OR REPLACE FUNCTION actualizar_inventario()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Inventario
    SET cantidad = cantidad - NEW.cantidad
    WHERE id_producto = NEW.id_producto;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_actualizar_inventario
AFTER INSERT ON Detalle_Venta
FOR EACH ROW
EXECUTE FUNCTION actualizar_inventario();

CREATE OR REPLACE FUNCTION validar_stock()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_stock_actual INT;
BEGIN
    SELECT cantidad INTO v_stock_actual
    FROM Inventario
    WHERE id_producto = NEW.id_producto;
    
    IF v_stock_actual < NEW.cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente para el producto ID %. Stock actual: %, Cantidad solicitada: %',
            NEW.id_producto, v_stock_actual, NEW.cantidad;
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_validar_stock
BEFORE INSERT ON Detalle_Venta
FOR EACH ROW
EXECUTE FUNCTION validar_stock();

CREATE TABLE auditoria_productos (
    id_auditoria SERIAL PRIMARY KEY,
    id_producto INT,
    accion VARCHAR(10),
    precio_anterior DECIMAL(10,2),
    precio_nuevo DECIMAL(10,2),
    usuario VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION registrar_cambio_producto()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.precio <> OLD.precio THEN
        INSERT INTO auditoria_productos(id_producto, accion, precio_anterior, precio_nuevo, usuario)
        VALUES (NEW.id_producto, 'UPDATE', OLD.precio, NEW.precio, current_user);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO auditoria_productos(id_producto, accion, precio_anterior, usuario)
        VALUES (OLD.id_producto, 'DELETE', OLD.precio, current_user);
    END IF;
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_auditoria_producto
AFTER UPDATE OR DELETE ON Productos
FOR EACH ROW
EXECUTE FUNCTION registrar_cambio_producto();

