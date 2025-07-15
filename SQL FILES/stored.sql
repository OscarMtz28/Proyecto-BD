CREATE OR REPLACE PROCEDURE reponer_inventario(
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Inventario
    SET cantidad = cantidad + p_cantidad,
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_producto = p_id_producto;
END;
    IF NOT FOUND THEN
        INSERT INTO Inventario(id_producto, cantidad, ubicacion)
        VALUES (p_id_producto, p_cantidad, 'Nueva ubicación');
    END IF;
$$;
