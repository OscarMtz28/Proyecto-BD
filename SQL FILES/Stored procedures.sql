CREATE OR REPLACE PROCEDURE registrar_venta(
    p_id_cliente INT,
    p_metodo_pago VARCHAR(50),
    p_detalles JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_venta INT;
    v_total DECIMAL(12,2) := 0;
    detalle JSONB;
BEGIN
    -- Calcular el total
    FOR detalle IN SELECT * FROM jsonb_array_elements(p_detalles)
    LOOP
        v_total := v_total + (detalle->>'cantidad')::INT * 
                  (SELECT precio FROM Productos WHERE id_producto = (detalle->>'id_producto')::INT);
    END LOOP;
    
    -- Insertar la venta
    INSERT INTO Ventas(id_cliente, total, metodo_pago)
    VALUES (p_id_cliente, v_total, p_metodo_pago)
    RETURNING id_venta INTO v_id_venta;
    
    -- Insertar detalles
    FOR detalle IN SELECT * FROM jsonb_array_elements(p_detalles)
    LOOP
        INSERT INTO Detalle_Venta(id_venta, id_producto, cantidad, precio_unitario)
        VALUES (
            v_id_venta,
            (detalle->>'id_producto')::INT,
            (detalle->>'cantidad')::INT,
            (SELECT precio FROM Productos WHERE id_producto = (detalle->>'id_producto')::INT)
        );
        
        -- Actualizar inventario
        UPDATE Inventario
        SET cantidad = cantidad - (detalle->>'cantidad')::INT
        WHERE id_producto = (detalle->>'id_producto')::INT;
    END LOOP;
    
    -- Actualizar puntos de fidelidad (5% del total)
    UPDATE Clientes
    SET puntos_fidelidad = puntos_fidelidad + (v_total * 0.05)::INT
    WHERE id_cliente = p_id_cliente;
    
    COMMIT;
END;
$$;

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
    
    IF NOT FOUND THEN
        INSERT INTO Inventario(id_producto, cantidad, ubicacion)
        VALUES (p_id_producto, p_cantidad, 'Nueva ubicación');
    END IF;
END;
$$;
