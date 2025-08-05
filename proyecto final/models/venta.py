"""
Modelo para la gestión de ventas
"""
from database.connection import DatabaseConnection

class VentaModel:
    """Modelo para operaciones de ventas"""
    
    @staticmethod
    def obtener_recientes(limit=50):
        """Obtener ventas recientes"""
        query = """SELECT v.id_venta, CONCAT(c.nombre, ' ', c.apellido), 
                          v.fecha_venta, v.total, v.metodo_pago
                   FROM Ventas v 
                   JOIN Clientes c ON v.id_cliente = c.id_cliente 
                   ORDER BY v.fecha_venta DESC LIMIT %s"""
        return DatabaseConnection.execute_query(query, (limit,), fetch=True)
    
    @staticmethod
    def crear_venta(cliente_id, total, metodo_pago, productos):
        """Crear nueva venta con sus detalles"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            
            # Insertar venta
            cursor.execute("""INSERT INTO Ventas (id_cliente, total, metodo_pago) 
                             VALUES (%s, %s, %s) RETURNING id_venta""",
                          (cliente_id, total, metodo_pago))
            venta_id = cursor.fetchone()[0]
            
            # Insertar detalles de venta
            for producto in productos:
                cursor.execute("""INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario) 
                                 VALUES (%s, %s, %s, %s)""",
                              (venta_id, producto['id'], producto['cantidad'], producto['precio']))
            
            conn.commit()
            return venta_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_productos_mas_vendidos(limit=10):
        """Obtener productos más vendidos"""
        query = """
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido, 
                   SUM(dv.subtotal) as ingresos_totales
            FROM Detalle_Venta dv
            JOIN Productos p ON dv.id_producto = p.id_producto
            GROUP BY p.id_producto, p.nombre
            ORDER BY total_vendido DESC
            LIMIT %s
        """
        return DatabaseConnection.execute_query(query, (limit,), fetch=True)
    
    @staticmethod
    def obtener_ventas_por_cliente(limit=15):
        """Obtener ventas agrupadas por cliente"""
        query = """
            SELECT CONCAT(c.nombre, ' ', c.apellido) as cliente, 
                   COUNT(v.id_venta) as num_compras,
                   SUM(v.total) as total_gastado,
                   c.puntos_fidelidad
            FROM Ventas v
            JOIN Clientes c ON v.id_cliente = c.id_cliente
            GROUP BY c.id_cliente, c.nombre, c.apellido, c.puntos_fidelidad
            ORDER BY total_gastado DESC
            LIMIT %s
        """
        return DatabaseConnection.execute_query(query, (limit,), fetch=True)
    
    @staticmethod
    def obtener_ventas_mes_actual():
        """Obtener ventas del mes actual"""
        query_diarias = """
            SELECT DATE(fecha_venta) as fecha, COUNT(*) as num_ventas, SUM(total) as total_dia
            FROM Ventas
            WHERE EXTRACT(MONTH FROM fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE)
              AND EXTRACT(YEAR FROM fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE)
            GROUP BY DATE(fecha_venta)
            ORDER BY fecha DESC
        """
        
        query_totales = """
            SELECT COUNT(*) as total_ventas, COALESCE(SUM(total), 0) as ingresos_totales
            FROM Ventas
            WHERE EXTRACT(MONTH FROM fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE)
              AND EXTRACT(YEAR FROM fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE)
        """
        
        try:
            ventas_diarias = DatabaseConnection.execute_query(query_diarias, fetch=True)
            totales = DatabaseConnection.execute_query(query_totales, fetch=True)
            
            # Debug: imprimir resultados
            print(f"Debug - Ventas diarias: {ventas_diarias}")
            print(f"Debug - Totales: {totales}")
            
            # Asegurar que siempre retornemos datos válidos
            if not ventas_diarias:
                ventas_diarias = []
            
            if totales and len(totales) > 0:
                return ventas_diarias, totales[0]
            else:
                return ventas_diarias, (0, 0.0)
                
        except Exception as e:
            print(f"Error en obtener_ventas_mes_actual: {e}")
            return [], (0, 0.0)
    
    @staticmethod
    def obtener_ventas_por_mes(mes, año):
        """Obtener ventas de un mes y año específicos"""
        query_diarias = """
            SELECT DATE(fecha_venta) as fecha, COUNT(*) as num_ventas, SUM(total) as total_dia
            FROM Ventas
            WHERE EXTRACT(MONTH FROM fecha_venta) = %s
              AND EXTRACT(YEAR FROM fecha_venta) = %s
            GROUP BY DATE(fecha_venta)
            ORDER BY fecha DESC
        """
        
        query_totales = """
            SELECT COUNT(*) as total_ventas, COALESCE(SUM(total), 0) as ingresos_totales
            FROM Ventas
            WHERE EXTRACT(MONTH FROM fecha_venta) = %s
              AND EXTRACT(YEAR FROM fecha_venta) = %s
        """
        
        try:
            ventas_diarias = DatabaseConnection.execute_query(query_diarias, (mes, año), fetch=True)
            totales = DatabaseConnection.execute_query(query_totales, (mes, año), fetch=True)
            
            # Asegurar que siempre retornemos datos válidos
            if not ventas_diarias:
                ventas_diarias = []
            
            if totales and len(totales) > 0:
                return ventas_diarias, totales[0]
            else:
                return ventas_diarias, (0, 0.0)
                
        except Exception as e:
            print(f"Error en obtener_ventas_por_mes: {e}")
            return [], (0, 0.0)
    
    @staticmethod
    def obtener_info_debug_ventas():
        """Obtener información de debug sobre las ventas"""
        queries = {
            'total_ventas': "SELECT COUNT(*) FROM Ventas",
            'ventas_recientes': "SELECT fecha_venta, total FROM Ventas ORDER BY fecha_venta DESC LIMIT 5",
            'fecha_actual': "SELECT CURRENT_DATE",
            'mes_actual': "SELECT EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)"
        }
        
        resultados = {}
        for nombre, query in queries.items():
            try:
                resultado = DatabaseConnection.execute_query(query, fetch=True)
                resultados[nombre] = resultado
            except Exception as e:
                resultados[nombre] = f"Error: {e}"
        
        return resultados