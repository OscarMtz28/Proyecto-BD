from dulceria_db import DulceriaDB
import json

def main():
    db = DulceriaDB()
    
    try:
        # 1. Agregar un nuevo producto
        nuevo_producto = db.agregar_producto(
            "Chocolate blanco",
            "Tableta 100g de chocolate blanco",
            38.50,
            "Chocolates"
        )
        print(f"Producto agregado con ID: {nuevo_producto[0]['id_producto']}")
        
        # 2. Registrar una venta
        detalles_venta = [
            {"id_producto": 1, "cantidad": 2},
            {"id_producto": 3, "cantidad": 1}
        ]
        
        if db.registrar_venta(1, detalles_venta, "Efectivo"):
            print("Venta registrada exitosamente")
        
        # 3. Obtener reporte de productos más vendidos
        mas_vendidos = db.productos_mas_vendidos()
        print("\nProductos más vendidos:")
        for producto in mas_vendidos:
            print(f"{producto['nombre']}: {producto['total_vendido']} unidades")
            
        # 4. Ventas del mes actual
        ventas_mes = db.ventas_mes_actual()
        print(f"\nVentas del mes actual: ${ventas_mes[0]['ventas_mes_actual'] or 0}")
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()