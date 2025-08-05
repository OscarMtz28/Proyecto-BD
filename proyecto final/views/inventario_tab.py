"""
Vista para la pestaña de inventario
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.inventario import InventarioModel
from models.producto import ProductoModel
from utils.validators import Validators
from utils.table_sorter import TableSorter

class InventarioTab:
    """Clase para manejar la pestaña de inventario"""
    
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        
        # Variables para control de ordenamiento
        self.sort_column = None
        self.sort_reverse = False
        
        # Variable para controlar actualizaciones automáticas
        self.auto_refresh_enabled = True
        
        self.setup_ui()
        self.cargar_datos_iniciales()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame superior para controles
        control_frame = tk.Frame(self.frame, bg='white', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="Gestión de Inventario", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Controles de reposición
        reposicion_frame = tk.Frame(control_frame, bg='white')
        reposicion_frame.pack(pady=10)
        
        tk.Label(reposicion_frame, text="Producto:", bg='white').pack(side='left', padx=5)
        self.producto_combo = ttk.Combobox(reposicion_frame, width=30, state='readonly')
        self.producto_combo.pack(side='left', padx=5)
        
        tk.Label(reposicion_frame, text="Cantidad a agregar:", bg='white').pack(side='left', padx=5)
        self.cantidad_entry = tk.Entry(reposicion_frame, width=10)
        self.cantidad_entry.pack(side='left', padx=5)
        
        tk.Label(reposicion_frame, text="Ubicación:", bg='white').pack(side='left', padx=5)
        self.ubicacion_entry = tk.Entry(reposicion_frame, width=15)
        self.ubicacion_entry.pack(side='left', padx=5)
        
        tk.Button(reposicion_frame, text="Reponer Stock", command=self.reponer_inventario, 
                 bg='#27ae60', fg='white').pack(side='left', padx=10)
        
        # Botones adicionales
        botones_frame = tk.Frame(control_frame, bg='white')
        botones_frame.pack(pady=5)
        
        tk.Button(botones_frame, text="Actualizar Inventario", command=self.cargar_inventario, 
                 bg='#3498db', fg='white', width=18).pack(side='left', padx=5)
        tk.Button(botones_frame, text="Limpiar Campos", command=self.limpiar_campos, 
                 bg='#95a5a6', fg='white', width=18).pack(side='left', padx=5)
        
        # Control de actualización automática
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_check = tk.Checkbutton(botones_frame, text="Actualización automática", 
                                          variable=self.auto_refresh_var, bg='white',
                                          command=self.toggle_auto_refresh)
        auto_refresh_check.pack(side='left', padx=10)
        
        # Indicador de última actualización
        self.status_label = tk.Label(botones_frame, text="", bg='white', fg='green', font=('Arial', 8))
        self.status_label.pack(side='left', padx=10)
        
        # Tabla de inventario
        table_frame = tk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columnas completas (incluye ID para funcionalidad interna)
        self.all_columns = ('ID', 'Producto', 'Cantidad', 'Ubicación', 'Última Actualización')
        self.tree = ttk.Treeview(table_frame, columns=self.all_columns, show='headings', height=20)
        
        # Configurar columnas (ocultar ID)
        for col in self.all_columns:
            if col == 'ID':
                # Ocultar completamente la columna ID
                self.tree.column(col, width=0, minwidth=0, stretch=False)
                self.tree.heading(col, text='')
            else:
                self.tree.heading(col, text=col, command=lambda c=col: self.ordenar_tabla(c))
                self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind para selección
        self.tree.bind('<ButtonRelease-1>', self.seleccionar_item)
    
    def cargar_datos_iniciales(self):
        """Cargar datos iniciales"""
        self.cargar_productos_combo()
        self.cargar_inventario()
    
    def cargar_productos_combo(self):
        """Cargar productos para el inventario"""
        try:
            productos = ProductoModel.obtener_activos()
            producto_values = [f"{producto[0]} - {producto[1]}" for producto in productos]
            self.producto_combo['values'] = producto_values
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def reponer_inventario(self):
        """Reponer stock de inventario"""
        if not self.producto_combo.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        # Validar cantidad
        es_valida, resultado = Validators.validar_cantidad(self.cantidad_entry.get())
        if not es_valida:
            messagebox.showerror("Error", resultado)
            return
        
        cantidad = resultado
        
        # Extraer ID del producto
        try:
            producto_info = self.producto_combo.get()
            producto_id = int(producto_info.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Formato de producto inválido")
            return
        
        ubicacion = self.ubicacion_entry.get() or 'Sin especificar'
        
        try:
            success = InventarioModel.reponer_stock(producto_id, cantidad, ubicacion)
            
            if success:
                messagebox.showinfo("Éxito", f"Inventario actualizado: +{cantidad} unidades")
                self.limpiar_campos()
                self.cargar_inventario()
                
                # Notificar actualización de inventario
                if self.app:
                    datos_inventario = {
                        'producto_id': producto_id,
                        'cantidad_agregada': cantidad,
                        'ubicacion': ubicacion
                    }
                    self.app.disparar_evento('inventario_actualizado', datos_inventario)
                
                self.actualizar_status(f"Stock repuesto: +{cantidad} unidades")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el inventario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al reponer inventario: {str(e)}")
    
    def limpiar_campos(self):
        """Limpiar campos del formulario"""
        self.producto_combo.set('')
        self.cantidad_entry.delete(0, tk.END)
        self.ubicacion_entry.delete(0, tk.END)
    
    def seleccionar_item(self, event):
        """Manejar selección de item en la tabla"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Mostrar información del item seleccionado
            producto_nombre = values[1]
            cantidad_actual = values[2]
            ubicacion_actual = values[3]
            
            # Opcional: Cargar datos en el formulario para facilitar actualización
            # Buscar el producto en el combo
            for value in self.producto_combo['values']:
                if producto_nombre in value:
                    self.producto_combo.set(value)
                    break
            
            if ubicacion_actual and ubicacion_actual != 'Sin especificar':
                self.ubicacion_entry.delete(0, tk.END)
                self.ubicacion_entry.insert(0, ubicacion_actual)
    
    def cargar_inventario(self):
        """Cargar inventario en la tabla"""
        try:
            inventario = InventarioModel.obtener_todo()
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar inventario
            for item in inventario:
                fecha_formateada = item[4].strftime("%Y-%m-%d %H:%M")
                
                # Colorear filas según el stock
                cantidad = item[2]
                tags = ()
                if cantidad < 10:
                    tags = ('stock_critico',)
                elif cantidad < 20:
                    tags = ('stock_bajo',)
                
                tree_item = self.tree.insert('', 'end', values=(
                    item[0], item[1], item[2], item[3] or 'Sin especificar', fecha_formateada
                ), tags=tags)
            
            # Configurar colores para las etiquetas
            self.tree.tag_configure('stock_critico', background='#ffcccc')  # Rojo claro
            self.tree.tag_configure('stock_bajo', background='#fff3cd')     # Amarillo claro
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inventario: {str(e)}")
    
    def ordenar_tabla(self, col):
        """Ordenar tabla por columna"""
        # Solo permitir ordenamiento en columnas visibles
        if col == 'ID':
            return
            
        self.sort_column, self.sort_reverse = TableSorter.sort_treeview(
            self.tree, col, self.sort_column, self.sort_reverse, 
            numeric_columns=['Cantidad']
        )
        
        TableSorter.update_header_indicators(self.tree, col, self.sort_reverse, self.all_columns)
    
    def obtener_estadisticas_inventario(self):
        """Obtener estadísticas básicas del inventario"""
        try:
            inventario = InventarioModel.obtener_todo()
            
            total_productos = len(inventario)
            stock_total = sum(item[2] for item in inventario)
            stock_bajo = len([item for item in inventario if item[2] < 20])
            stock_critico = len([item for item in inventario if item[2] < 10])
            
            return {
                'total_productos': total_productos,
                'stock_total': stock_total,
                'stock_bajo': stock_bajo,
                'stock_critico': stock_critico
            }
        except Exception:
            return None
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas del inventario"""
        stats = self.obtener_estadisticas_inventario()
        if stats:
            mensaje = f"""ESTADÍSTICAS DEL INVENTARIO:
            
Total de productos: {stats['total_productos']}
Stock total: {stats['stock_total']} unidades
Productos con stock bajo (<20): {stats['stock_bajo']}
Productos con stock crítico (<10): {stats['stock_critico']}"""
            
            messagebox.showinfo("Estadísticas de Inventario", mensaje)
    
    def toggle_auto_refresh(self):
        """Alternar actualización automática"""
        self.auto_refresh_enabled = self.auto_refresh_var.get()
        status = "activada" if self.auto_refresh_enabled else "desactivada"
        self.actualizar_status(f"Actualización automática {status}")
    
    def actualizar_status(self, mensaje):
        """Actualizar el mensaje de status"""
        self.status_label.config(text=mensaje)
        # Limpiar el mensaje después de 3 segundos
        self.frame.after(3000, lambda: self.status_label.config(text=""))
    
    def actualizar_despues_venta(self, datos_venta=None):
        """Actualizar inventario después de realizar una venta"""
        if not self.auto_refresh_enabled:
            return
        
        try:
            # Actualizar el inventario
            self.cargar_inventario()
            
            # Mostrar mensaje de actualización
            if datos_venta:
                productos_vendidos = len(datos_venta.get('productos', []))
                self.actualizar_status(f"Inventario actualizado - Venta procesada ({productos_vendidos} productos)")
            else:
                self.actualizar_status("Inventario actualizado automáticamente")
                
            # Opcional: Resaltar productos con stock bajo después de la venta
            self.resaltar_stock_bajo()
            
        except Exception as e:
            print(f"Error al actualizar inventario después de venta: {e}")
            self.actualizar_status("Error al actualizar inventario")
    
    def resaltar_stock_bajo(self):
        """Resaltar productos con stock bajo después de una actualización"""
        try:
            # Contar productos con stock bajo
            stock_bajo_count = 0
            stock_critico_count = 0
            
            for item_id in self.tree.get_children():
                item = self.tree.item(item_id)
                cantidad = int(item['values'][2])
                
                if cantidad < 10:
                    stock_critico_count += 1
                elif cantidad < 20:
                    stock_bajo_count += 1
            
            # Mostrar alerta si hay productos con stock crítico
            if stock_critico_count > 0:
                self.frame.after(1000, lambda: messagebox.showwarning(
                    "Stock Crítico", 
                    f"¡ATENCIÓN! {stock_critico_count} producto(s) con stock crítico (<10 unidades).\n"
                    f"Revise el inventario y considere reabastecer."
                ))
            elif stock_bajo_count > 0:
                self.actualizar_status(f"Advertencia: {stock_bajo_count} producto(s) con stock bajo")
                
        except Exception as e:
            print(f"Error al verificar stock bajo: {e}")