"""
Modelo para la gestión de clientes
"""
from database.connection import DatabaseConnection

class ClienteModel:
    """Modelo para operaciones CRUD de clientes"""
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los clientes"""
        query = "SELECT id_cliente, nombre, apellido, telefono, email, puntos_fidelidad FROM Clientes ORDER BY apellido, nombre"
        return DatabaseConnection.execute_query(query, fetch=True)
    
    @staticmethod
    def obtener_para_combo():
        """Obtener clientes para combobox"""
        query = "SELECT id_cliente, nombre, apellido FROM Clientes ORDER BY apellido, nombre"
        return DatabaseConnection.execute_query(query, fetch=True)
    
    @staticmethod
    def crear(nombre, apellido, telefono, email, direccion):
        """Crear nuevo cliente"""
        query = """INSERT INTO Clientes (nombre, apellido, telefono, email, direccion) 
                  VALUES (%s, %s, %s, %s, %s)"""
        return DatabaseConnection.execute_query(query, (nombre, apellido, telefono, email, direccion))
    
    @staticmethod
    def actualizar(cliente_id, nombre, apellido, telefono, email, direccion):
        """Actualizar cliente existente"""
        query = """UPDATE Clientes SET nombre=%s, apellido=%s, telefono=%s, email=%s, direccion=%s 
                  WHERE id_cliente=%s"""
        return DatabaseConnection.execute_query(query, (nombre, apellido, telefono, email, direccion, cliente_id))
    
    @staticmethod
    def eliminar(cliente_id):
        """Eliminar cliente"""
        query = "DELETE FROM Clientes WHERE id_cliente=%s"
        return DatabaseConnection.execute_query(query, (cliente_id,))
    
    @staticmethod
    def obtener_direccion(cliente_id):
        """Obtener dirección completa del cliente"""
        query = "SELECT direccion FROM Clientes WHERE id_cliente=%s"
        result = DatabaseConnection.execute_query(query, (cliente_id,), fetch=True)
        return result[0][0] if result and result[0][0] else ""