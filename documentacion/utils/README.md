# Módulo Utils

## Descripción
Este módulo contiene utilidades y funciones auxiliares reutilizables que son utilizadas por múltiples componentes del sistema. Proporciona funcionalidades comunes que mejoran la experiencia del usuario y la robustez del sistema.

## Archivos

### `__init__.py`
- Archivo de inicialización del paquete
- Permite importar el módulo como paquete Python

### `validators.py`
**Propósito**: Centralizar todas las validaciones de datos del sistema.

**Funcionalidades esperadas**:
- ✅ Validación robusta de datos en todos los formularios
- Validaciones específicas por tipo de dato
- Mensajes de error estandarizados
- Validaciones de reglas de negocio

**Tipos de validaciones**:

#### Validaciones Básicas
- **Campos requeridos**: Verificar que no estén vacíos
- **Tipos de datos**: Números, fechas, emails, teléfonos
- **Longitud**: Mínima y máxima de cadenas
- **Formato**: Patrones específicos (email, teléfono)

#### Validaciones de Negocio
- **Precios**: Valores positivos, formato monetario
- **Stock**: Cantidades válidas, no negativos
- **Fechas**: Rangos válidos, fechas futuras/pasadas
- **Códigos**: Unicidad, formato específico

#### Validaciones de Base de Datos
- **Duplicados**: Verificar registros únicos
- **Referencias**: Validar claves foráneas
- **Integridad**: Consistencia de datos

**Métodos típicos**:
```python
def validar_email(email):
    """Valida formato de email"""
    
def validar_telefono(telefono):
    """Valida formato de teléfono"""
    
def validar_precio(precio):
    """Valida que el precio sea positivo"""
    
def validar_stock(cantidad):
    """Valida cantidad de stock"""
    
def validar_fecha(fecha):
    """Valida formato y rango de fecha"""
    
def validar_campo_requerido(valor, nombre_campo):
    """Valida que un campo no esté vacío"""
```



## Características Comunes

### Manejo de Errores
- Excepciones específicas por tipo de error
- Mensajes de error claros y útiles
- Logging de errores para debugging


## Uso Típico

### Validators
```python
from utils.validators import validar_email, validar_precio

# Validar email
if not validar_email(email_input):
    mostrar_error("Email inválido")

# Validar precio
try:
    precio_validado = validar_precio(precio_input)
except ValueError as e:
    mostrar_error(str(e))
```


## Beneficios del Diseño

### Reutilización
- Funciones utilizadas en múltiples módulos
- Evita duplicación de código
- Consistencia en toda la aplicación

### Mantenibilidad
- Cambios centralizados
- Fácil agregar nuevas validaciones
- Testing independiente

### Extensibilidad
- Fácil agregar nuevos tipos de validación
- Configuración flexible

### Robustez
- Validaciones
- Manejo consistente de errores

## Integración con el Sistema
- Utilizado por todas las vistas para validación
- Integrado en formularios automáticamente
- Configuración centralizada de reglas de negocio
