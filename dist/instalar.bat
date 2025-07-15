@echo off
echo ========================================
echo    Sistema de Gestión - Dulcería
echo    Instalador y Configurador
echo ========================================
echo.

echo Verificando PostgreSQL...
pg_isready >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL no está ejecutándose
    echo Por favor, inicia PostgreSQL antes de continuar
    pause
    exit /b 1
)

echo ✅ PostgreSQL detectado

echo.
echo Configurando base de datos...
echo Asegúrate de haber ejecutado los scripts SQL antes de continuar
echo.

echo ✅ Configuración completada
echo.
echo Para ejecutar la aplicación:
echo   1. Ejecuta SistemaDulceria.exe
echo   2. Configura la conexión en config.py si es necesario
echo.
pause
