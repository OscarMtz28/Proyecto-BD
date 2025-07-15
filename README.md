# Sistema de Gestión - Dulcería

Una aplicación de escritorio desarrollada en Python con tkinter para la gestión completa de una dulcería, incluyendo productos, clientes, ventas e inventario.

## Características

- **Gestión de Productos**: Agregar, editar y eliminar productos con categorías
- **Gestión de Clientes**: Registro de clientes con sistema de puntos de fidelidad
- **Sistema de Ventas**: Procesamiento de ventas con múltiples productos y métodos de pago
- **Control de Inventario**: Seguimiento de stock y reposición de productos
- **Reportes**: Estadísticas de ventas, productos más vendidos y análisis de clientes

## Requisitos del Sistema

- Python 3.7 o superior
- PostgreSQL 12 o superior
- Librerías Python (ver requirements.txt)

## Instalación

### 1. Configurar la Base de Datos

Primero, asegúrate de tener PostgreSQL instalado y ejecutándose.

```sql
-- Crear la base de datos
CREATE DATABASE dulceria;

-- Conectarse a la base de datos y ejecutar los scripts SQL
\c dulceria;

-- Ejecutar en orden:
-- 1. SQL FILES/Crear tablas.sql
-- 2. SQL FILES/Indices.sql
-- 3. SQL FILES/Stored procedures.sql
-- 4. SQL FILES/Trigers.sql
-- 5. SQL FILES/Agregar productos.sql (datos de ejemplo)
```

### 2. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

### 3. Configurar la Conexión

Edita el archivo `config.py` y actualiza los datos de conexión a tu base de datos:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'dulceria',
    'user': 'tu_usuario',
    'password': 'tu_password',
    'port': 5432
}
```

### 4. Ejecutar la Aplicación

```bash
python main.py
```

## Uso de la Aplicación

### Pestaña Productos
- **Agregar**: Completa los campos y haz clic en "Agregar"
- **Editar**: Selecciona un producto de la tabla, modifica los campos y haz clic en "Actualizar"
- **Eliminar**: Selecciona un producto y haz clic en "Eliminar" (se desactiva, no se borra)

### Pestaña Clientes
- **Registro**: Ingresa los datos del cliente y haz clic en "Agregar"
- **Edición**: Selecciona un cliente, modifica los datos y actualiza
- **Puntos de Fidelidad**: Se actualizan automáticamente con las compras

### Pestaña Ventas
- **Nueva Venta**: 
  1. Selecciona un cliente
  2. Elige el método de pago
  3. Agrega productos con sus cantidades
  4. Procesa la venta
- **Historial**: Ve todas las ventas realizadas en la tabla inferior

### Pestaña Inventario
- **Reposición**: Selecciona un producto, ingresa la cantidad y ubicación
- **Seguimiento**: Ve el stock actual de todos los productos

### Pestaña Reportes
- **Productos Más Vendidos**: Top 10 de productos por cantidad vendida
- **Ventas por Cliente**: Ranking de clientes por compras realizadas
- **Stock Bajo**: Productos con menos de 20 unidades
- **Ventas del Mes**: Resumen de ventas del mes actual

## Estructura del Proyecto

```
proyecto-dulceria/
├── main.py                 # Aplicación principal
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
├── SQL FILES/            # Scripts de base de datos
│   ├── Crear tablas.sql
│   ├── Indices.sql
│   ├── Stored procedures.sql
│   ├── Trigers.sql
│   └── Agregar productos.sql
└── imagenes/             # Recursos gráficos
    ├── logo.png
    └── ubi.png
```

## Funcionalidades Avanzadas

### Stored Procedures
La aplicación utiliza procedimientos almacenados para:
- Procesamiento de ventas con actualización automática de puntos de fidelidad
- Reposición de inventario

### Triggers
- Auditoría automática de cambios en productos
- Validaciones de integridad de datos

### Índices
- Optimización de consultas frecuentes
- Mejora del rendimiento en búsquedas

## Solución de Problemas

### Error de Conexión a la Base de Datos
1. Verifica que PostgreSQL esté ejecutándose
2. Confirma los datos de conexión en `config.py`
3. Asegúrate de que la base de datos `dulceria` exista

### Error de Módulos
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problemas de Permisos
Asegúrate de que el usuario de PostgreSQL tenga permisos para:
- Crear y modificar tablas
- Ejecutar procedimientos almacenados
- Insertar, actualizar y eliminar datos

## Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un pull request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Contacto

Para soporte o preguntas sobre el proyecto, contacta al desarrollador.