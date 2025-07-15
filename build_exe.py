#!/usr/bin/env python3
"""
Script para crear ejecutable de la aplicación Dulcería
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Construir el ejecutable usando PyInstaller"""
    
    print("🚀 Iniciando proceso de construcción del ejecutable...")
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado")
    
    # Limpiar builds anteriores
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("🧹 Limpiando builds anteriores")
    
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Comando de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name=SistemaDulceria",      # Nombre del ejecutable
        "--add-data=config.py;.",      # Incluir archivo de configuración
        "--hidden-import=psycopg2",    # Importación oculta necesaria
        "--hidden-import=tkinter",     # Importación oculta necesaria
        "main.py"
    ]
    
    # Agregar icono si existe
    if os.path.exists("imagenes/logo.png"):
        print("🎨 Icono encontrado, agregando al ejecutable...")
        # Nota: PyInstaller necesita .ico, no .png
        # cmd.extend(["--icon=imagenes/logo.ico"])
    
    print("🔨 Ejecutando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Ejecutable creado exitosamente!")
        print(f"📁 Ubicación: {os.path.abspath('dist/SistemaDulceria.exe')}")
        
        # Mostrar tamaño del archivo
        exe_path = Path("dist/SistemaDulceria.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 Tamaño: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print("❌ Error al crear el ejecutable:")
        print(e.stderr)
        return False
    
    # Limpiar archivos temporales
    if os.path.exists("SistemaDulceria.spec"):
        os.remove("SistemaDulceria.spec")
        print("🧹 Archivos temporales limpiados")
    
    print("\n🎉 ¡Proceso completado!")
    print("📋 Instrucciones:")
    print("   1. El ejecutable está en la carpeta 'dist/'")
    print("   2. Asegúrate de tener PostgreSQL instalado en el sistema destino")
    print("   3. Configura la conexión a la base de datos antes de distribuir")
    
    return True

def create_installer_script():
    """Crear script de instalación/configuración mejorado"""
    installer_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo    Sistema de Gestión - Dulcería
echo    Instalador y Configurador v1.0
echo ========================================
echo.

echo [1/4] Verificando PostgreSQL...
pg_isready >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL no está ejecutándose o no está instalado
    echo.
    echo Soluciones:
    echo   - Inicia el servicio PostgreSQL
    echo   - Verifica que PostgreSQL esté instalado
    echo   - Ejecuta: net start postgresql-x64-XX
    echo.
    pause
    exit /b 1
)
echo ✅ PostgreSQL detectado y ejecutándose

echo.
echo [2/4] Verificando base de datos 'dulceria'...
psql -U postgres -d dulceria -c "SELECT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Base de datos 'dulceria' no encontrada
    echo.
    echo IMPORTANTE: Debes crear la base de datos primero:
    echo   1. Abre pgAdmin o psql
    echo   2. Ejecuta: CREATE DATABASE dulceria;
    echo   3. Ejecuta los scripts SQL en orden:
    echo      - SQL FILES/Crear tablas.sql
    echo      - SQL FILES/Indices.sql  
    echo      - SQL FILES/Stored procedures.sql
    echo      - SQL FILES/Trigers.sql
    echo      - SQL FILES/Agregar productos.sql (opcional)
    echo.
    echo Presiona cualquier tecla para continuar sin verificar...
    pause >nul
) else (
    echo ✅ Base de datos 'dulceria' encontrada
)

echo.
echo [3/4] Verificando configuración...
if exist "config.py" (
    echo ✅ Archivo de configuración encontrado
    echo.
    echo RECUERDA: Edita config.py con tus credenciales:
    echo   - Usuario de PostgreSQL
    echo   - Contraseña
    echo   - Puerto (si es diferente a 5432)
) else (
    echo ⚠️  Archivo config.py no encontrado
    echo La aplicación podría no funcionar correctamente
)

echo.
echo [4/4] Configuración completada
echo ========================================
echo.
echo 🚀 PARA USAR LA APLICACIÓN:
echo   1. Edita config.py con tus credenciales de PostgreSQL
echo   2. Ejecuta SistemaDulceria.exe
echo   3. Si hay errores de conexión, verifica config.py
echo.
echo 📁 ARCHIVOS IMPORTANTES:
echo   - SistemaDulceria.exe (aplicación principal)
echo   - config.py (configuración de base de datos)
echo   - SQL FILES/ (scripts de base de datos)
echo.
echo 📞 SOPORTE:
echo   - Verifica que PostgreSQL esté ejecutándose
echo   - Revisa las credenciales en config.py
echo   - Asegúrate de que la base de datos 'dulceria' exista
echo.
echo ¡Presiona cualquier tecla para finalizar!
pause >nul
'''
    
    with open("dist/instalar.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("📦 Script de instalación mejorado creado: dist/instalar.bat")

if __name__ == "__main__":
    if build_executable():
        create_installer_script()
        print("\n🚀 ¡Todo listo para distribuir!")