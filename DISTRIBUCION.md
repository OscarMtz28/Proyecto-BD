# 📦 Guía de Distribución - Sistema Dulcería

## 🚀 Crear Ejecutable

### **Opción 1: Script Automático (Recomendado)**
```bash
python build_exe.py
```

### **Opción 2: PyInstaller Manual**
```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable básico
pyinstaller --onefile --windowed main.py

# Crear ejecutable con configuración personalizada
pyinstaller dulceria.spec
```

### **Opción 3: Comando Completo**
```bash
pyinstaller --onefile --windowed --name=SistemaDulceria --add-data="config.py;." --hidden-import=psycopg2 main.py
```

## 📋 **Requisitos del Sistema Destino**

### **Software Necesario:**
- Windows 10/11 (64-bit)
- PostgreSQL 12+ instalado y ejecutándose
- Drivers de PostgreSQL (incluidos con PostgreSQL)

### **Hardware Mínimo:**
- RAM: 4GB
- Espacio: 100MB libres
- Procesador: Dual-core 2GHz+

## 🗂️ **Estructura de Distribución**

```
SistemaDulceria/
├── SistemaDulceria.exe     # Ejecutable principal
├── config.py               # Configuración (editable)
├── instalar.bat           # Script de instalación
├── imagenes/              # Recursos gráficos
│   ├── logo.png
│   └── ubi.png
├── SQL FILES/             # Scripts de base de datos
│   ├── Crear tablas.sql
│   ├── Indices.sql
│   ├── Stored procedures.sql
│   ├── Trigers.sql
│   └── Agregar productos.sql
└── README_INSTALACION.txt # Instrucciones para el usuario
```

## ⚙️ **Configuración para Distribución**

### **1. Preparar config.py para distribución:**
```python
# config.py - Versión para distribución
DB_CONFIG = {
    'host': 'localhost',
    'database': 'dulceria',
    'user': 'postgres',
    'password': '',  # El usuario debe configurar
    'port': 5432
}
```

### **2. Crear archivo de configuración inicial:**
```python
# config_template.py
DB_CONFIG_TEMPLATE = {
    'host': 'localhost',
    'database': 'dulceria', 
    'user': 'TU_USUARIO_AQUI',
    'password': 'TU_PASSWORD_AQUI',
    'port': 5432
}
```

## 📦 **Métodos de Distribución**

### **Método 1: Carpeta Completa**
1. Crear carpeta `SistemaDulceria`
2. Copiar ejecutable y archivos necesarios
3. Comprimir en ZIP
4. Distribuir con instrucciones

### **Método 2: Instalador (Avanzado)**
Usar herramientas como:
- **Inno Setup** (Windows)
- **NSIS** (Nullsoft Scriptable Install System)
- **WiX Toolset** (Windows Installer XML)

### **Método 3: Portable**
- Un solo ejecutable
- Configuración mediante archivo externo
- No requiere instalación

## 🔧 **Solución de Problemas Comunes**

### **Error: "No module named 'psycopg2'"**
```bash
# Agregar importación oculta
pyinstaller --hidden-import=psycopg2 main.py
```

### **Error: "tkinter not found"**
```bash
# Verificar instalación de tkinter
python -m tkinter
```

### **Ejecutable muy grande**
```bash
# Usar UPX para comprimir
pyinstaller --onefile --upx-dir=/path/to/upx main.py
```

### **Error de conexión a BD**
- Verificar que PostgreSQL esté ejecutándose
- Comprobar credenciales en config.py
- Verificar que la base de datos 'dulceria' exista

## 📝 **Lista de Verificación Pre-Distribución**

- [ ] Ejecutable se crea sin errores
- [ ] Aplicación inicia correctamente
- [ ] Conexión a base de datos funciona
- [ ] Todas las pestañas cargan
- [ ] CRUD de productos funciona
- [ ] CRUD de clientes funciona
- [ ] Sistema de ventas funciona
- [ ] Inventario se actualiza
- [ ] Reportes se generan
- [ ] Archivos SQL incluidos
- [ ] Documentación completa
- [ ] Script de instalación funciona

## 🚀 **Comandos Rápidos**

```bash
# Desarrollo
python main.py

# Crear ejecutable rápido
pyinstaller --onefile --windowed main.py

# Crear ejecutable completo
python build_exe.py

# Limpiar archivos temporales
rmdir /s build dist
del *.spec
```

## 📞 **Soporte**

Para problemas de distribución:
1. Verificar logs de PyInstaller
2. Comprobar dependencias
3. Revisar configuración de BD
4. Consultar documentación de PostgreSQL

---
**Nota:** Siempre prueba el ejecutable en un sistema limpio antes de distribuir.