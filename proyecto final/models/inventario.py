"""
Modelo para la gestión de inventario
"""
from database.connection import DatabaseConnection

class InventarioModel:
    """Modelo para operaciones de inventario"""
    
    @staticmethod
    def obtener_todo():
        """Obtener todo el inventario"""
        query = """SELECT i.id_inventario, p.nombre, i.cantidad, i.ubicacion, i.fecha_actualizacion
                   FROM Inventario i 
                   JOIN Productos p ON i.id_producto = p.id_producto 
                   ORDER BY p.nombre"""
        return DatabaseConnection.execute_query(query, fetch=True)
    
    @staticmethod
    def reponer_stock(producto_id, cantidad, ubicacion):
        """Reponer stock de un producto"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # Verificar si ya existe registro de inventario
            cursor.execute("SELECT id_inventario, cantidad FROM Inventario WHERE id_producto=%s", (producto_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Actualizar cantidad existente
                cursor.execute("""UPDATE Inventario SET cantidad = cantidad + %s, 
                                 fecha_actualizacion = CURRENT_TIMESTAMP, ubicacion = %s 
                                 WHERE id_producto = %s""",
                              (cantidad, ubicacion, producto_id))
            else:
                # Crear nuevo registro
                cursor.execute("""INSERT INTO Inventario (id_producto, cantidad, ubicacion) 
                                 VALUES (%s, %s, %s)""",
                              (producto_id, cantidad, ubicacion))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_stock_bajo(limite=20):
        """Obtener productos con stock bajo"""
        query = """
            SELECT p.nombre, i.cantidad, i.ubicacion, p.categoria
            FROM Inventario i
            JOIN Productos p ON i.id_producto = p.id_producto
            WHERE i.cantidad < %s
            ORDER BY i.cantidad ASC
        """
        return DatabaseConnection.execute_query(query, (limite,), fetch=True)