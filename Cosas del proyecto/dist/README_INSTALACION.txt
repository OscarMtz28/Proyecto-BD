========================================
    SISTEMA DE GESTIÓN - DULCERÍA
    Guía de Instalación y Uso
========================================

📋 REQUISITOS DEL SISTEMA
========================================
- Windows 10/11 (64-bit)
- PostgreSQL 12 o superior
- 4GB de RAM mínimo
- 100MB de espacio libre en disco

🚀 INSTALACIÓN PASO A PASO
========================================

PASO 1: Verificar PostgreSQL
----------------------------
1. Asegúrate de que PostgreSQL esté instalado
2. Verifica que el servicio esté ejecutándose
3. Anota tu usuario y contraseña de PostgreSQL

PASO 2: Crear la Base de Datos
------------------------------
1. Abre pgAdmin o la consola psql
2. Ejecuta: CREATE DATABASE dulceria;
3. Ejecuta los siguientes scripts EN ORDEN:
   a) SQL FILES/Crear tablas.sql
   b) SQL FILES/Indices.sql
   c) SQL FILES/Stored procedures.sql
   d) SQL FILES/Trigers.sql
   e) SQL FILES/Agregar productos.sql (datos de ejemplo)

PASO 3: Configurar la Conexión
------------------------------
1. Abre el archivo config.py con un editor de texto
2. Modifica los siguientes valores:
   - 'user': 'tu_usuario_postgresql'
   - 'password': 'tu_contraseña_postgresql'
   - 'host': 'localhost' (normalmente no cambiar)
   - 'port': 5432 (normalmente no cambiar)

PASO 4: Ejecutar el Instalador
------------------------------
1. Haz doble clic en instalar.bat
2. Sigue las instrucciones en pantalla
3. El instalador verificará que todo esté correcto

PASO 5: Iniciar la Aplicación
-----------------------------
1. Haz doble clic en SistemaDulceria.exe
2. La aplicación debería abrir sin errores
3. ¡Ya puedes comenzar a usar el sistema!

🎯 PRIMER USO
========================================

Al abrir la aplicación verás 5 pestañas:

1. PRODUCTOS
   - Agregar nuevos productos
   - Editar precios y descripciones
   - Organizar por categorías

2. CLIENTES
   - Registrar clientes
   - Sistema de puntos de fidelidad
   - Historial de compras

3. VENTAS
   - Procesar ventas rápidamente
   - Múltiples productos por venta
   - Diferentes métodos de pago

4. INVENTARIO
   - Control de stock
   - Reposición de productos
   - Ubicaciones en tienda

5. REPORTES
   - Productos más vendidos
   - Análisis de clientes
   - Control de stock bajo
   - Resumen mensual

🔧 SOLUCIÓN DE PROBLEMAS
========================================

ERROR: "No se pudo conectar a la base de datos"
-----------------------------------------------
✅ Verifica que PostgreSQL esté ejecutándose
✅ Revisa las credenciales en config.py
✅ Confirma que la base de datos 'dulceria' exista
✅ Verifica el puerto (normalmente 5432)

ERROR: "Módulo no encontrado"
-----------------------------
✅ Ejecuta instalar.bat nuevamente
✅ Verifica que todos los archivos estén presentes
✅ Contacta soporte técnico

ERROR: La aplicación no inicia
------------------------------
✅ Verifica que tengas permisos de administrador
✅ Desactiva temporalmente el antivirus
✅ Ejecuta como administrador

APLICACIÓN LENTA
-----------------
✅ Verifica que PostgreSQL tenga suficiente memoria
✅ Cierra otras aplicaciones pesadas
✅ Considera actualizar el hardware

📞 SOPORTE TÉCNICO
========================================

Si tienes problemas:

1. Ejecuta instalar.bat para diagnóstico automático
2. Verifica la lista de solución de problemas
3. Anota el mensaje de error exacto
4. Contacta al administrador del sistema

📁 ARCHIVOS IMPORTANTES
========================================

SistemaDulceria.exe    - Aplicación principal
config.py              - Configuración de base de datos
instalar.bat          - Verificador del sistema
SQL FILES/            - Scripts de base de datos
imagenes/             - Recursos gráficos

⚠️  IMPORTANTE: No elimines ningún archivo

🎉 ¡LISTO PARA USAR!
========================================

Una vez completada la instalación, tu sistema de dulcería estará listo para:

✅ Gestionar productos y precios
✅ Registrar clientes y puntos de fidelidad
✅ Procesar ventas rápidamente
✅ Controlar inventario automáticamente
✅ Generar reportes de negocio

¡Disfruta usando tu nuevo sistema de gestión!

========================================
Sistema de Gestión - Dulcería v1.0
Copyright © 2025
========================================