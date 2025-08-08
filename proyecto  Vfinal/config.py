# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'dulceria',
    'user': 'postgres',
    'password': 'Magia2000',
    'port': 5432
}

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Sistema de dulceria',
    'geometry': '1400x800',
    'version': '2.0.0 - Modular'
}

# Configuración de reportes
REPORTS_CONFIG = {
    'default_export_path': './reportes/',
    'company_name': 'Dulceria amor',
    'company_address': 'Jose Maria Castorena',
    'company_phone': '515151515'
}

# Configuración de inventario
INVENTORY_CONFIG = {
    'stock_bajo_limite': 20,
    'stock_critico_limite': 10,
    'ubicacion_default': 'Almacén Principal'
}