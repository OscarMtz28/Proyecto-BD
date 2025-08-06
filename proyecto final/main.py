"""
Aplicación principal modular para el Sistema de Gestión de Dulcería
"""
import tkinter as tk
from tkinter import ttk
from config import APP_CONFIG
from views.productos_tab import ProductosTab
from views.clientes_tab import ClientesTab
from views.ventas_tab import VentasTab
from views.inventario_tab import InventarioTab
from views.reportes_tab import ReportesTab

class DulceriaApp:
    """Aplicación principal del sistema de dulcería"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(APP_CONFIG['geometry'])
        self.root.configure(bg='#f0f0f0')
        
        # Sistema de eventos para comunicación entre pestañas
        self.event_callbacks = {
            'venta_realizada': [],
            'producto_actualizado': [],
            'inventario_actualizado': []
        }
        
        self.setup_ui()
    
    def registrar_callback(self, evento, callback):
        """Registrar un callback para un evento específico"""
        if evento in self.event_callbacks:
            self.event_callbacks[evento].append(callback)
    
    def disparar_evento(self, evento, datos=None):
        """Disparar un evento y ejecutar todos los callbacks registrados"""
        if evento in self.event_callbacks:
            for callback in self.event_callbacks[evento]:
                try:
                    if datos:
                        callback(datos)
                    else:
                        callback()
                except Exception as e:
                    print(f"Error en callback para evento {evento}: {e}")
        
    def setup_ui(self):
        """Configurar la interfaz de usuario principal"""
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Sistema de Gestión - Dulcería", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_tabs()
        
    def create_tabs(self):
        """Crear todas las pestañas de la aplicación"""
        # Pestaña de productos
        self.productos_tab = ProductosTab(self.notebook, self)
        self.notebook.add(self.productos_tab.frame, text="Productos")
        
        # Pestaña de clientes
        self.clientes_tab = ClientesTab(self.notebook, self)
        self.notebook.add(self.clientes_tab.frame, text="Clientes")
        
        # Pestaña de ventas
        self.ventas_tab = VentasTab(self.notebook, self)
        self.notebook.add(self.ventas_tab.frame, text="Ventas")
        
        # Pestaña de inventario
        self.inventario_tab = InventarioTab(self.notebook, self)
        self.notebook.add(self.inventario_tab.frame, text="Inventario")
        
        # Pestaña de reportes
        self.reportes_tab = ReportesTab(self.notebook, self)
        self.notebook.add(self.reportes_tab.frame, text="Reportes")
        
        # Configurar eventos entre pestañas
        self.setup_eventos()
    
    def setup_eventos(self):
        """Configurar eventos entre pestañas"""
        # Cuando se realiza una venta, actualizar inventario
        self.registrar_callback('venta_realizada', self.inventario_tab.actualizar_despues_venta)
        
        # Cuando se actualiza un producto, refrescar inventario
        self.registrar_callback('producto_actualizado', self.inventario_tab.cargar_inventario)

if __name__ == "__main__":
    root = tk.Tk()
    app = DulceriaApp(root)
    root.mainloop()