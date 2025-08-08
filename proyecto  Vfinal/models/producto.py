"""
Modelo para la gestión de productos
"""
from database.connection import DatabaseConnection

class ProductoModel:
    """Modelo para operaciones CRUD de productos"""
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los productos"""
        query = "SELECT id_producto, nombre, descripcion, precio, categoria, activo FROM Productos ORDER BY nombre"
        return DatabaseConnection.execute_query(query, fetch=True)
    
    @staticmethod
    def obtener_activos():
        """Obtener solo productos activos"""
        query = "SELECT id_producto, nombre, precio FROM Productos WHERE activo=TRUE ORDER BY nombre"
        return DatabaseConnection.execute_query(query, fetch=True)
    
    @staticmethod
    def crear(nombre, descripcion, precio, categoria):
        """Crear nuevo producto"""
        query = """INSERT INTO Productos (nombre, descripcion, precio, categoria) 
                  VALUES (%s, %s, %s, %s)"""
        return DatabaseConnection.execute_query(query, (nombre, descripcion, precio, categoria))
    
    @staticmethod
    def actualizar(producto_id, nombre, descripcion, precio, categoria):
        """Actualizar producto existente"""
        query = """UPDATE Productos SET nombre=%s, descripcion=%s, precio=%s, categoria=%s 
                  WHERE id_producto=%s"""
        return DatabaseConnection.execute_query(query, (nombre, descripcion, precio, categoria, producto_id))
    
    @staticmethod
    def eliminar_cascada(producto_id):
        """Eliminar producto en cascada"""
        queries = [
            ("DELETE FROM Detalle_Venta WHERE id_producto=%s", (producto_id,)),
            ("DELETE FROM Inventario WHERE id_producto=%s", (producto_id,)),
            ("DELETE FROM Productos WHERE id_producto=%s", (producto_id,))
        ]
        return DatabaseConnection.execute_transaction(queries)
    
    @staticmethod
    def reactivar(producto_id):
        """Reactivar producto"""
        query = "UPDATE Productos SET activo=TRUE WHERE id_producto=%s"
        return DatabaseConnection.execute_query(query, (producto_id,))
    
    @staticmethod
    def obtener_info_eliminacion(producto_id):
        """Obtener información sobre registros relacionados antes de eliminar"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None, None
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Detalle_Venta WHERE id_producto=%s", (producto_id,))
            ventas_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Inventario WHERE id_producto=%s", (producto_id,))
            inventario_count = cursor.fetchone()[0]
            
            return ventas_count, inventario_count
        finally:
            conn.close()