# Módulo Reports

## Descripción
Este módulo se encarga de la generación de reportes del sistema, específicamente la creación de documentos PDF con información analítica y estadística del negocio.

## Archivos

### `__init__.py`
- Archivo de inicialización del paquete
- Permite importar el módulo como paquete Python

### `pdf_generator.py`
**Propósito**: Generar reportes profesionales en formato PDF con datos del sistema.

## Clase Principal: `PDFGenerator`

### Constructor
```python
def __init__(self, filename):
```
- **Parámetros**: `filename` - Nombre del archivo PDF a generar
- **Funcionalidad**: 
  - Inicializa el documento PDF con tamaño A4
  - Configura estilos de texto predefinidos
  - Crea estilo personalizado para títulos

### Métodos de Configuración

#### `agregar_titulo(titulo)`
- **Propósito**: Agregar título principal al reporte
- **Características**:
  - Estilo personalizado con fuente grande
  - Color azul oscuro
  - Centrado en la página
  - Espaciado automático

#### `agregar_fecha()`
- **Propósito**: Agregar fecha y hora de generación
- **Formato**: "dd/mm/yyyy HH:MM"
- **Posición**: Debajo del título

#### `agregar_parrafo(texto, estilo='Normal')`
- **Propósito**: Agregar texto descriptivo
- **Parámetros**:
  - `texto`: Contenido del párrafo
  - `estilo`: Estilo de texto (Normal, Heading1, etc.)

#### `agregar_tabla(data, col_widths=None)`
- **Propósito**: Crear tablas con formato profesional
- **Características**:
  - Header con fondo gris y texto blanco
  - Filas alternadas con fondo beige
  - Bordes y alineación automática
  - Anchos de columna personalizables

### Métodos de Generación de Reportes

#### `generar_productos_vendidos(datos)`
**Propósito**: Reporte de productos más vendidos

**Estructura de datos esperada**:
```python
datos = [
    (nombre_producto, cantidad_vendida, ingresos_totales),
    ...
]
```

**Contenido del reporte**:
- Título: "REPORTE DE PRODUCTOS MÁS VENDIDOS"
- Fecha de generación
- Tabla con columnas:
  - Producto
  - Cantidad Vendida
  - Ingresos Totales (formato monetario)

**Manejo de datos**:
- Validación de valores None
- Formato monetario automático
- Mensaje cuando no hay datos

#### `generar_ventas_cliente(datos)`
**Propósito**: Reporte de ventas por cliente

**Estructura de datos esperada**:
```python
datos = [
    (nombre_cliente, num_compras, total_gastado, puntos_acumulados),
    ...
]
```

**Contenido del reporte**:
- Título: "REPORTE DE VENTAS POR CLIENTE"
- Fecha de generación
- Tabla con columnas:
  - Cliente
  - Compras realizadas
  - Total Gastado (formato monetario)
  - Puntos acumulados

#### `generar_stock_bajo(datos)`
**Propósito**: Reporte de productos con stock bajo

**Estructura de datos esperada**:
```python
datos = [
    (nombre_producto, stock_actual, ubicacion, categoria),
    ...
]
```

**Contenido del reporte**:
- Título: "REPORTE DE PRODUCTOS CON STOCK BAJO"
- Fecha de generación
- Tabla con columnas:
  - Producto
  - Stock actual
  - Ubicación
  - Categoría
- Mensaje positivo si no hay productos con stock bajo

#### `generar_ventas_mes(datos_diarios, totales)`
**Propósito**: Reporte de ventas del mes actual

**Parámetros**:
- `datos_diarios`: Ventas día por día
- `totales`: Resumen de totales del mes

#### `generar_ventas_mes_personalizado(datos_diarios, totales, periodo)`
**Propósito**: Reporte de ventas para período personalizado

**Parámetros**:
- `datos_diarios`: Ventas del período
- `totales`: Resumen de totales
- `periodo`: Descripción del período

### Método de Finalización

#### `guardar()`
- **Propósito**: Generar y guardar el archivo PDF
- **Funcionalidad**: Construye el documento con todos los elementos agregados

## Tecnologías Utilizadas

### ReportLab
- **SimpleDocTemplate**: Estructura del documento
- **Paragraph**: Texto con formato
- **Table**: Tablas con estilos
- **Spacer**: Espaciado entre elementos
- **getSampleStyleSheet**: Estilos predefinidos

### Características del PDF

#### Formato
- **Tamaño**: A4
- **Orientación**: Vertical
- **Márgenes**: Estándar
- **Fuentes**: Helvetica (estándar PDF)

#### Estilos Visuales
- **Títulos**: Azul oscuro, centrados, fuente grande
- **Tablas**: Headers grises, filas beige alternadas
- **Texto**: Negro estándar, bien espaciado

## Características Principales


- Construcción paso a paso del documento
- Métodos encadenables para agregar elementos
- Flexibilidad en el orden de construcción


- Estructura común para todos los reportes
- Métodos específicos para cada tipo
- Reutilización de componentes comunes


- Creación de diferentes tipos de reportes
- Configuración automática según el tipo
- Extensible para nuevos reportes

## Uso 

```python
from reports.pdf_generator import PDFGenerator

# Crear generador
pdf = PDFGenerator("reporte_productos.pdf")

# Agregar contenido
pdf.agregar_titulo("Mi Reporte")
pdf.agregar_fecha()
pdf.generar_productos_vendidos(datos_productos)

# Guardar archivo
pdf.guardar()
```

## Características Destacadas

### Robustez
- Manejo seguro de valores None
- Validación de datos de entrada
- Mensajes informativos cuando no hay datos

### Profesionalismo
- Formato empresarial estándar
- Colores y tipografía consistentes
- Estructura clara y legible

### Flexibilidad
- Anchos de columna personalizables
- Múltiples tipos de reporte
- Fácil extensión para nuevos formatos

## Integración con el Sistema
- Utilizado por `reportes_tab.py` para exportación
- Datos proporcionados por los modelos
- Generación bajo demanda del usuario

## Beneficios
- **Profesionalismo**: Reportes con calidad empresarial
- **Automatización**: Generación automática de PDFs
- **Consistencia**: Formato uniforme en todos los reportes
- **Extensibilidad**: Fácil agregar nuevos tipos de reporte