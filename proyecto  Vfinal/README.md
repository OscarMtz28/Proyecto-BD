# Sistema de Gestión de Dulcería - Versión Modular

## Estructura del Proyecto

```
dulceria/
├── main_modular.py          # Aplicación principal modular
├── main.py                  # Aplicación original (monolítica)
├── config.py                # Configuración de la aplicación
├── README.md               # Este archivo
│
├── database/               # Módulos de base de datos
│   ├── __init__.py
│   └── connection.py       # Manejo de conexiones DB
│
├── models/                 # Modelos de datos
│   ├── __init__.py
│   ├── producto.py         # Modelo de productos
│   ├── cliente.py          # Modelo de clientes
│   ├── venta.py           # Modelo de ventas
│   └── inventario.py      # Modelo de inventario
│
├── views/                  # Interfaces de usuario
│   ├── __init__.py
│   ├── productos_tab.py    # Pestaña de productos
│   ├── clientes_tab.py     # Pestaña de clientes
│   ├── ventas_tab.py       # Pestaña de ventas
│   ├── inventario_tab.py   # Pestaña de inventario
│   └── reportes_tab.py     # Pestaña de reportes
│
├── utils/                  # Utilidades
│   ├── __init__.py
│   ├── validators.py       # Validadores de datos
│   └── table_sorter.py     # Ordenamiento de tablas
│
└── reports/                # Generación de reportes
    ├── __init__.py
    └── pdf_generator.py    # Generador de PDFs
```

## Características de la Modularización

### 1. **Separación de Responsabilidades**
- **Models**: Lógica de negocio y acceso a datos
- **Views**: Interfaces de usuario
- **Utils**: Funciones auxiliares reutilizables
- **Database**: Manejo centralizado de conexiones
- **Reports**: Generación de reportes

### 2. **Beneficios**
- **Mantenibilidad**: Código más fácil de mantener y debuggear
- **Reutilización**: Componentes reutilizables entre módulos
- **Escalabilidad**: Fácil agregar nuevas funcionalidades
- **Testeo**: Cada módulo se puede testear independientemente
- **Colaboración**: Múltiples desarrolladores pueden trabajar en paralelo

### 3. **Patrones Implementados**
- **MVC (Model-View-Controller)**: Separación clara de capas
- **Repository Pattern**: Modelos encapsulan acceso a datos
- **Factory Pattern**: Generación de reportes PDF
- **Utility Classes**: Funciones auxiliares centralizadas

## Uso

### Ejecutar la versión modular:
```bash
python main_modular.py
```

### Ejecutar la versión original:
```bash
python main.py
```

## Estado del Proyecto

### 🎉 **Modularización Completa**

Todas las funcionalidades han sido exitosamente modularizadas:

- ✅ **Productos** - Gestión completa de productos
- ✅ **Clientes** - Gestión completa de clientes  
- ✅ **Ventas** - Sistema de ventas con búsqueda de productos
- ✅ **Inventario** - Control de stock con alertas visuales
- ✅ **Reportes** - Generación y exportación a PDF
- ✅ **Base de datos** - Conexiones centralizadas
- ✅ **Validadores** - Funciones de validación reutilizables
- ✅ **Utilidades** - Ordenamiento de tablas y más

### 🚀 **Funcionalidades Destacadas**

- **Búsqueda en tiempo real** de productos en ventas
- **Alertas visuales** para stock bajo/crítico en inventario
- **Validación robusta** de datos en todos los formularios
- **Ordenamiento dinámico** en todas las tablas
- **Exportación a PDF** de todos los reportes
- **Eliminación en cascada** con confirmaciones detalladas

## Dependencias

- tkinter (incluido en Python)
- psycopg2 (para PostgreSQL)
- reportlab (para generación de PDFs)

## Configuración

Asegúrate de que el archivo `config.py` contenga la configuración correcta de la base de datos y la aplicación.