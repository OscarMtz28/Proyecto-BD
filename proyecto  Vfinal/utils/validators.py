"""
Utilidades para validación de datos
"""
import re

class Validators:
    """Clase con métodos de validación"""
    
    @staticmethod
    def validar_producto(nombre, precio):
        """Validar datos de producto"""
        errors = []
        
        if not nombre.strip():
            errors.append("El nombre es obligatorio")
        
        try:
            precio_float = float(precio)
            if precio_float <= 0:
                errors.append("El precio debe ser mayor a 0")
        except ValueError:
            errors.append("El precio debe ser un número válido")
        
        return errors
    
    @staticmethod
    def validar_cliente(nombre, apellido, email=None):
        """Validar datos de cliente"""
        errors = []
        
        if not nombre.strip():
            errors.append("El nombre es obligatorio")
        
        if not apellido.strip():
            errors.append("El apellido es obligatorio")
        
        if email and email.strip():
            if not Validators._validar_email(email):
                errors.append("El formato del email no es válido")
        
        return errors
    
    @staticmethod
    def validar_cantidad(cantidad_str):
        """Validar cantidad numérica"""
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a 0"
            return True, cantidad
        except ValueError:
            return False, "La cantidad debe ser un número entero positivo"
    
    @staticmethod
    def _validar_email(email):
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None