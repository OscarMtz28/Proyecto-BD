# Módulo Models

## Descripción
Este módulo contiene los modelos de datos que representan las entidades del negocio y encapsulan la lógica de acceso a datos para cada tabla de la base de datos.

## Archivos

### `__init__.py`
- Archivo de inicialización del paquete
- Permite importar el módulo como paquete Python

### `producto.py`
**Propósito**: Modelo para la gestión de productos de la dulcería.

**Funcionalidades esperadas**:
- CRUD completo de productos
- Validación de datos de productos
- Consultas específicas de productos

**Métodos**:
- `crear()`
- `obtener_todos()`
- `obtener_activos()`
- `actualizar()`
- `eliminar()`
- `listar_productos()`


### `cliente.py`
**Propósito**: Modelo para la gestión de clientes.

**Funcionalidades esperadas**:
- CRUD completo de clientes
- Validación de datos personales

**Métodos **:
- `crear()`
- `obtener(id)`
- `obtener_todos()`
- `actualizar()`
- `eliminar_cliente()`
- `obtener_direccion()`


### `venta.py`
**Propósito**: Modelo para el registro y gestión de ventas.

**Funcionalidades**:
- Registro de ventas
- Cálculo de totales
- Gestión de detalles de venta
- Actualización automática de inventario

**Métodos típicos**:
- `crear_venta()`
- `obtener_recientes()`
- `obtener_productos_mas_vendidos()`
- `obtener_ventas_por_cliente()`
- `obtener_venta_mes_actual()`

### `inventario.py`
**Propósito**: Modelo para el control de stock e inventario.

**Funcionalidades**:
- Control de stock en tiempo real
- Alertas de stock bajo
- Movimientos de inventario
- Reportes de stock

**Métodos**:
- `obtener_todo()`
- `reponer_stock()`
- `obtener_stock_bajo()`

### Características principales

- Cada modelo encapsula el acceso a su tabla correspondiente
- Abstrae las consultas SQL específicas
- Proporciona una interfaz limpia para las vistas

- Los modelos representan tanto datos como comportamiento
- Métodos para persistir y recuperar datos
- Validaciones integradas en el modelo

- Creación consistente de objetos de modelo
- Inicialización con valores por defecto

## Características Comunes

### Validación de Datos
- Validación de tipos de datos
- Validación de reglas de negocio
- Manejo de errores de validación

### Manejo de Errores
- Excepciones específicas por tipo de error
- Logging de operaciones críticas
- Rollback automático en transacciones

### Optimización
- Consultas optimizadas
- Uso de índices apropiados

## Uso
```python
from models.producto import Producto
from models.cliente import Cliente
from models.venta import Venta

# Crear un producto
producto = Producto()
producto.crear_producto("Chocolate", "Dulces", 2.50, 100)

# Obtener cliente
cliente = Cliente.obtener_cliente(1)

# Registrar venta
venta = Venta()
venta.crear_venta(cliente_id=1, productos=[...])
```

## Integración con Database
- Todos los modelos utilizan `DatabaseConnection` para acceso a datos
- Consultas preparadas para seguridad
- Transacciones para operaciones complejas

## Beneficios
- **Reutilización**: Lógica de negocio centralizada
- **Mantenibilidad**: Cambios aislados por entidad
- **Testabilidad**: Cada modelo se puede testear independientemente
- **Escalabilidad**: Fácil agregar nuevas entidades