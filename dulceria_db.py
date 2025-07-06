import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from config import DB_CONFIG

class DulceriaDB:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("Conexión exitosa a PostgreSQL")
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            raise
    
    def disconnect(self):
        """Cierra la conexión"""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")
    
    def execute_query(self, query, params=None, fetch=False):
        """Ejecuta una consulta genérica"""
        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error en la consulta: {e}")
            raise
    
    # Métodos específicos para productos
    def agregar_producto(self, nombre, descripcion, precio, categoria):
        query = """
        INSERT INTO Productos (nombre, descripcion, precio, categoria)
        VALUES (%s, %s, %s, %s)
        RETURNING id_producto;
        """
        return self.execute_query(query, (nombre, descripcion, precio, categoria), fetch=True)
    
    def obtener_productos(self):
        query = "SELECT * FROM Productos WHERE activo = TRUE;"
        return self.execute_query(query, fetch=True)
    
    # Métodos para ventas
    def registrar_venta(self, id_cliente, detalles, metodo_pago):
        """Implementa el stored procedure de registrar_venta"""
        try:
            with self.connection.cursor() as cursor:
                # Convertimos los detalles a formato JSON
                detalles_json = json.dumps(detalles)
                
                cursor.callproc(
                    'registrar_venta',
                    (id_cliente, metodo_pago, detalles_json)
                )
                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error al registrar venta: {e}")
            return False
    
    # Métodos para reportes
    def ventas_mes_actual(self):
        query = """
        SELECT SUM(total) AS ventas_mes_actual
        FROM Ventas
        WHERE date_trunc('month', fecha_venta) = date_trunc('month', CURRENT_DATE);
        """
        return self.execute_query(query, fetch=True)
    
    def productos_mas_vendidos(self, limite=5):
        query = """
        SELECT p.nombre, SUM(dv.cantidad) AS total_vendido
        FROM Detalle_Venta dv
        JOIN Productos p ON dv.id_producto = p.id_producto
        GROUP BY p.nombre
        ORDER BY total_vendido DESC
        LIMIT %s;
        """
        return self.execute_query(query, (limite,), fetch=True)