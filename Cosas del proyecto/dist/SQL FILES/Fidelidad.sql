CREATE VIEW puntos_clientes AS
SELECT id_cliente, nombre, apellido, puntos_fidelidad,
       puntos_fidelidad / 100 AS equivalente_en_pesos
FROM Clientes
ORDER BY puntos_fidelidad DESC;


select * from puntos_clientes order by puntos_fidelidad DESC;