"""
Módulo para manejo de conexiones a la base de datos
"""
import psycopg2
from tkinter import messagebox
from config import DB_CONFIG

class DatabaseConnection:
    """Clase para manejar conexiones a la base de datos"""
    
    @staticmethod
    def get_connection():
        """Establece conexión con la base de datos"""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Ejecuta una consulta y retorna el resultado"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def execute_transaction(queries_with_params):
        """Ejecuta múltiples consultas en una transacción"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN")
            
            for query, params in queries_with_params:
                cursor.execute(query, params)
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()