@echo off
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
