# Módulo Views

## Descripción
Este módulo contiene todas las interfaces de usuario (pestañas) del sistema. Cada archivo representa una pestaña específica de la aplicación con su funcionalidad completa.

## Archivos

### `__init__.py`
- Archivo de inicialización del paquete
- Permite importar el módulo como paquete Python

### `productos_tab.py`
**Propósito**: Interfaz para la gestión completa de productos.

**Funcionalidades**:
- CRUD completo de productos
- Formularios de alta/edición de productos
- Lista/tabla de productos existentes
- Búsqueda y filtrado de productos
- Validación de datos en tiempo real

**Componentes UI**:
- Formulario de producto (nombre, categoría, precio, descripción)
- Tabla con lista de productos
- Botones de acción (Agregar, Editar, Eliminar)
- Campo de búsqueda
- Filtros por categoría

### `clientes_tab.py`
**Propósito**: Interfaz para la gestión de clientes y sistema de fidelidad.

**Funcionalidades**:
- CRUD completo de clientes
- Sistema de puntos de fidelidad
- Historial de compras por cliente
- Búsqueda de clientes
- Validación de datos personales


### `ventas_tab.py`
**Propósito**: Interfaz para el registro y gestión de ventas.

**Funcionalidades**:
- Sistema completo de ventas
- Búsqueda en tiempo real de productos
- Selección de cliente
- Cálculo automático de totales
- Registro de transacciones


**Características destacadas**:
- Búsqueda instantánea mientras escribes
- Validación de stock disponible
- Actualización automática de inventario

### `inventario_tab.py`
**Propósito**: Control y monitoreo del inventario en tiempo real.

**Funcionalidades**:
- Control completo de stock
- Alertas visuales para stock bajo/crítico
- Movimientos de inventario
- Actualización de stock
- Reportes de inventario

**Componentes UI**:
- Tabla de inventario con códigos de color
- Indicadores visuales de stock:
  - Rojo: Stock crítico (< 10)
  - Amarillo: Stock bajo (< 20)
  - Verde: Stock normal
- Formularios de ajuste de stock
- Filtros por estado de stock

**Sistema de eventos**:
- Se actualiza automáticamente después de cada venta
- Responde a cambios en productos

### `reportes_tab.py`
**Propósito**: Generación y visualización de reportes del negocio.

**Funcionalidades**:
- Múltiples tipos de reportes
- Exportación a PDF de todos los reportes
- Filtros por fecha y período
- Visualización de datos estadísticos

**Tipos de reportes**:
1. **Productos más vendidos**
2. **Ventas por cliente**
3. **Stock bajo**
4. **Ventas del mes**
5. **Ventas por período personalizado**

**Componentes UI**:
- Selector de tipo de reporte
- Filtros de fecha
- Tabla de resultados
- Botón de exportar a PDF
- Gráficos y estadísticas

## Patrones de Diseño Implementados

### MVC (Model-View-Controller)
- Las vistas se enfocan solo en la presentación
- Delegan lógica de negocio a los modelos
- Controladores manejan la interacción usuario

### Observer Pattern
- Sistema de eventos entre pestañas
- Actualización automática cuando cambian los datos
- Comunicación desacoplada

### Command Pattern
- Botones y acciones encapsuladas
- Fácil agregar/modificar funcionalidades

## Sistema de Eventos

### Eventos Disponibles
- `venta_realizada`: Se dispara al completar una venta
- `producto_actualizado`: Se dispara al modificar un producto
- `inventario_actualizado`: Se dispara al cambiar stock

### Comunicación Entre Pestañas
```python
# Registrar callback
app.registrar_callback('venta_realizada', self.actualizar_inventario)

# Disparar evento
app.disparar_evento('venta_realizada', datos_venta)
```

## Características Comunes

### Validación de Datos
- Validación robusta en todos los formularios
- Mensajes de error claros
- Prevención de datos inválidos


### Búsqueda y Filtrado
- Búsqueda en tiempo real
- Filtros múltiples
- Resultados instantáneos

### Confirmaciones
- Eliminación con confirmaciones detalladas
- Diálogos de confirmación para acciones críticas

## Tecnologías Utilizadas
- **tkinter**: Framework de interfaz gráfica
- **ttk**: Widgets modernos de tkinter
- **threading**: Para operaciones no bloqueantes
- **datetime**: Manejo de fechas

## Integración
- Todas las vistas utilizan los modelos para acceso a datos
- Sistema de eventos centralizado en la aplicación principal
- Comunicación bidireccional entre pestañas

## Beneficios del Diseño
- **Modularidad**: Cada pestaña es independiente
- **Reutilización**: Componentes comunes compartidos
- **Mantenibilidad**: Fácil modificar funcionalidades específicas
- **Escalabilidad**: Agregar nuevas pestañas es sencillo