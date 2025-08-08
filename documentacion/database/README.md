# Módulo Database

## Descripción
Este módulo se encarga del manejo centralizado de conexiones a la base de datos PostgreSQL y la ejecución de consultas SQL.

## Archivos

### `__init__.py`
- Archivo de inicialización del paquete
- Permite importar el módulo como paquete Python

### `connection.py`
Contiene la clase principal para el manejo de la base de datos.

#### Clase: `DatabaseConnection`
**Propósito**: Proporcionar una interfaz centralizada para todas las operaciones de base de datos.

**Métodos principales**:

##### `get_connection()` (static)
- **Función**: Establece conexión con PostgreSQL
- **Parámetros**: Ninguno
- **Retorna**: Objeto de conexión o None si falla
- **Características**:
  - Utiliza configuración externa (`DB_CONFIG`)
  - Manejo de errores con interfaz gráfica
  - Muestra mensajes de error al usuario

##### `execute_query(query, params=None, fetch=False)` (static)
- **Función**: Ejecuta consultas SQL de forma segura
- **Parámetros**:
  - `query`: Consulta SQL a ejecutar
  - `params`: Parámetros para consultas preparadas (opcional)
  - `fetch`: True para SELECT, False para INSERT/UPDATE/DELETE
- **Retorna**: 
  - Si `fetch=True`: Lista de resultados
  - Si `fetch=False`: Número de filas afectadas
- **Características**:
  - Consultas preparadas (previene SQL injection)
  - Rollback automático en caso de error
  - Cierre garantizado de conexiones
  - Manejo robusto de excepciones

## Patrones de Diseño Implementados

### Singleton Pattern
- Una sola conexión por operación
- Métodos estáticos para acceso global

### Repository Pattern
- Abstrae el acceso a datos
- Centraliza la lógica de base de datos

## Tecnologías Utilizadas
- **PostgreSQL**: Sistema de gestión de base de datos
- **psycopg2**: Driver de Python para PostgreSQL
- **tkinter.messagebox**: Para mostrar errores al usuario

## Uso Típico
```python
from database.connection import DatabaseConnection

# Para consultas SELECT
resultados = DatabaseConnection.execute_query(
    "SELECT * FROM productos WHERE categoria = %s", 
    ("dulces",), 
    fetch=True
)

# Para INSERT/UPDATE/DELETE
filas_afectadas = DatabaseConnection.execute_query(
    "INSERT INTO productos (nombre, precio) VALUES (%s, %s)",
    ("Chocolate", 2.50)
)
```

## Ventajas del Diseño
- **Seguridad**: Consultas preparadas
- **Robustez**: Manejo integral de errores
- **Reutilización**: Acceso centralizado
- **Mantenibilidad**: Código limpio y organizado