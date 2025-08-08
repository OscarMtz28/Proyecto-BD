"""
Vista para la pestaña de ventas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.venta import VentaModel
from models.cliente import ClienteModel
from models.producto import ProductoModel
from utils.validators import Validators
from utils.table_sorter import TableSorter

class VentasTab:
    """Clase para manejar la pestaña de ventas"""
    
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        
        # Variables para control de ordenamiento
        self.sort_column = None
        self.sort_reverse = False
        
        # Lista de productos en la venta actual
        self.productos_venta = []
        
        # Lista completa de productos para filtrado
        self.productos_completos = []
        
        self.setup_ui()
        self.cargar_datos_iniciales()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame superior para nueva venta
        form_frame = tk.Frame(self.frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Nueva Venta", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Selección de cliente
        cliente_frame = tk.Frame(form_frame, bg='white')
        cliente_frame.pack(pady=5)
        
        tk.Label(cliente_frame, text="Cliente:", bg='white').pack(side='left', padx=5)
        self.cliente_combo = ttk.Combobox(cliente_frame, width=40, state='readonly')
        self.cliente_combo.pack(side='left', padx=5)
        
        tk.Label(cliente_frame, text="Método de Pago:", bg='white').pack(side='left', padx=5)
        self.metodo_pago_combo = ttk.Combobox(cliente_frame, width=20, values=['Efectivo', 'Tarjeta', 'Transferencia'])
        self.metodo_pago_combo.pack(side='left', padx=5)
        
        # Selección de productos
        productos_frame = tk.Frame(form_frame, bg='white')
        productos_frame.pack(pady=10, fill='x')
        
        tk.Label(productos_frame, text="Agregar Producto:", bg='white').pack(anchor='w', padx=5)
        
        producto_select_frame = tk.Frame(productos_frame, bg='white')
        producto_select_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(producto_select_frame, text="Producto:", bg='white').pack(side='left')
        self.producto_combo = ttk.Combobox(producto_select_frame, width=30)
        self.producto_combo.pack(side='left', padx=5)
        
        # Configurar búsqueda en tiempo real
        self.producto_combo.bind('<KeyRelease>', self.filtrar_productos)
        self.producto_combo.bind('<Button-1>', self.mostrar_todos_productos)
        self.producto_combo.bind('<FocusIn>', self.mostrar_todos_productos)
        
        tk.Label(producto_select_frame, text="Cantidad:", bg='white').pack(side='left', padx=5)
        self.cantidad_entry = tk.Entry(producto_select_frame, width=10)
        self.cantidad_entry.pack(side='left', padx=5)
        
        tk.Button(producto_select_frame, text="Agregar", command=self.agregar_producto_venta, 
                 bg='#27ae60', fg='white').pack(side='left', padx=5)
        
        # Tabla de productos en venta
        venta_table_frame = tk.Frame(form_frame, bg='white')
        venta_table_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns_venta = ('Producto', 'Precio', 'Cantidad', 'Subtotal')
        self.venta_tree = ttk.Treeview(venta_table_frame, columns=columns_venta, show='headings', height=6)
        
        for col in columns_venta:
            self.venta_tree.heading(col, text=col)
            self.venta_tree.column(col, width=120)
        
        self.venta_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar_venta = ttk.Scrollbar(venta_table_frame, orient='vertical', command=self.venta_tree.yview)
        self.venta_tree.configure(yscrollcommand=scrollbar_venta.set)
        scrollbar_venta.pack(side='right', fill='y')
        
        # Total y botones
        total_frame = tk.Frame(form_frame, bg='white')
        total_frame.pack(pady=10)
        
        self.total_label = tk.Label(total_frame, text="Total: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.total_label.pack(side='left', padx=20)
        
        tk.Button(total_frame, text="Procesar Venta", command=self.procesar_venta, 
                 bg='#2980b9', fg='white', width=15).pack(side='left', padx=10)
        tk.Button(total_frame, text="Limpiar", command=self.limpiar_venta, 
                 bg='#95a5a6', fg='white', width=15).pack(side='left', padx=10)
        
        # Tabla de ventas realizadas
        ventas_realizadas_frame = tk.Frame(self.frame)
        ventas_realizadas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(ventas_realizadas_frame, text="Ventas Realizadas", font=('Arial', 14, 'bold')).pack(pady=5)
        
        # Columnas completas (incluye ID para funcionalidad interna)
        self.all_columns_ventas = ('ID', 'Cliente', 'Fecha', 'Total', 'Método Pago')
        self.ventas_tree = ttk.Treeview(ventas_realizadas_frame, columns=self.all_columns_ventas, show='headings', height=10)
        
        # Configurar columnas (ocultar ID)
        for col in self.all_columns_ventas:
            if col == 'ID':
                # Ocultar completamente la columna ID
                self.ventas_tree.column(col, width=0, minwidth=0, stretch=False)
                self.ventas_tree.heading(col, text='')
            else:
                self.ventas_tree.heading(col, text=col, command=lambda c=col: self.ordenar_tabla(c))
                self.ventas_tree.column(col, width=150)
        
        scrollbar_ventas = ttk.Scrollbar(ventas_realizadas_frame, orient='vertical', command=self.ventas_tree.yview)
        self.ventas_tree.configure(yscrollcommand=scrollbar_ventas.set)
        
        self.ventas_tree.pack(side='left', fill='both', expand=True)
        scrollbar_ventas.pack(side='right', fill='y')
    
    def cargar_datos_iniciales(self):
        """Cargar datos iniciales para combos y tabla"""
        self.cargar_clientes_combo()
        self.cargar_productos_combo()
        self.cargar_ventas()
    
    def cargar_clientes_combo(self):
        """Cargar clientes en el combobox"""
        try:
            clientes = ClienteModel.obtener_para_combo()
            cliente_values = [f"{cliente[0]} - {cliente[1]} {cliente[2]}" for cliente in clientes]
            self.cliente_combo['values'] = cliente_values
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
    
    def cargar_productos_combo(self):
        """Cargar productos en el combobox"""
        try:
            productos = ProductoModel.obtener_activos()
            producto_values = [f"{producto[0]} - {producto[1]} (${producto[2]})" for producto in productos]
            
            # Guardar lista completa para filtrado
            self.productos_completos = producto_values.copy()
            
            # Configurar valores en el combobox
            self.producto_combo['values'] = producto_values
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def agregar_producto_venta(self):
        """Agregar producto a la venta actual"""
        if not self.producto_combo.get() or not self.cantidad_entry.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto y especifique la cantidad")
            return
        
        # Validar cantidad
        es_valida, resultado = Validators.validar_cantidad(self.cantidad_entry.get())
        if not es_valida:
            messagebox.showerror("Error", resultado)
            return
        
        cantidad = resultado
        
        # Extraer información del producto
        producto_info = self.producto_combo.get()
        try:
            producto_id = int(producto_info.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Formato de producto inválido")
            return
        
        try:
            # Obtener información del producto desde la base de datos
            productos = ProductoModel.obtener_activos()
            producto_encontrado = None
            
            for prod in productos:
                if prod[0] == producto_id:
                    producto_encontrado = prod
                    break
            
            if producto_encontrado:
                nombre = producto_encontrado[1]
                precio = producto_encontrado[2]
                subtotal = precio * cantidad
                
                # Agregar a la lista de productos de la venta
                self.productos_venta.append({
                    'id': producto_id,
                    'nombre': nombre,
                    'precio': precio,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
                
                # Actualizar tabla
                self.actualizar_tabla_venta()
                
                # Limpiar campos
                self.producto_combo.set('')
                self.cantidad_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Producto no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def actualizar_tabla_venta(self):
        """Actualizar la tabla de productos en venta"""
        # Limpiar tabla
        for item in self.venta_tree.get_children():
            self.venta_tree.delete(item)
        
        # Insertar productos
        total = 0
        for producto in self.productos_venta:
            self.venta_tree.insert('', 'end', values=(
                producto['nombre'],
                f"${producto['precio']:.2f}",
                producto['cantidad'],
                f"${producto['subtotal']:.2f}"
            ))
            total += producto['subtotal']
        
        # Actualizar total
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def procesar_venta(self):
        """Procesar la venta actual"""
        if not self.cliente_combo.get():
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return
        
        if not self.metodo_pago_combo.get():
            messagebox.showwarning("Advertencia", "Seleccione un método de pago")
            return
        
        if not self.productos_venta:
            messagebox.showwarning("Advertencia", "Agregue al menos un producto a la venta")
            return
        
        # Extraer ID del cliente
        try:
            cliente_info = self.cliente_combo.get()
            cliente_id = int(cliente_info.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Cliente inválido")
            return
        
        # Calcular total
        total = sum(producto['subtotal'] for producto in self.productos_venta)
        
        try:
            venta_id = VentaModel.crear_venta(
                cliente_id, 
                total, 
                self.metodo_pago_combo.get(), 
                self.productos_venta
            )
            
            if venta_id:
                messagebox.showinfo("Éxito", f"Venta procesada correctamente. ID: {venta_id}")
                
                # Notificar a otras pestañas sobre la venta realizada
                if self.app:
                    datos_venta = {
                        'venta_id': venta_id,
                        'cliente_id': cliente_id,
                        'total': total,
                        'productos': self.productos_venta.copy()
                    }
                    self.app.disparar_evento('venta_realizada', datos_venta)
                
                self.limpiar_venta()
                self.cargar_ventas()
            else:
                messagebox.showerror("Error", "No se pudo procesar la venta")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar venta: {str(e)}")
    
    def limpiar_venta(self):
        """Limpiar formulario de venta"""
        self.cliente_combo.set('')
        self.metodo_pago_combo.set('')
        self.producto_combo.set('')
        self.cantidad_entry.delete(0, tk.END)
        self.productos_venta = []
        self.actualizar_tabla_venta()
    
    def filtrar_productos(self, event):
        """Filtrar productos en tiempo real mientras se escribe"""
        if not hasattr(self, 'productos_completos') or not self.productos_completos:
            return
            
        texto_busqueda = self.producto_combo.get().lower().strip()
        
        if not texto_busqueda:
            productos_filtrados = self.productos_completos
        else:
            productos_filtrados = [
                producto for producto in self.productos_completos
                if texto_busqueda in producto.lower()
            ]
        
        # Actualizar los valores del combobox
        self.producto_combo['values'] = productos_filtrados
        
        # Si hay resultados y hay texto de búsqueda, mostrar el dropdown
        if productos_filtrados and texto_busqueda:
            try:
                self.producto_combo.event_generate('<Button-1>')
                self.producto_combo.event_generate('<ButtonRelease-1>')
            except:
                pass
    
    def mostrar_todos_productos(self, event):
        """Mostrar todos los productos cuando se hace clic en el combobox"""
        if hasattr(self, 'productos_completos') and self.productos_completos:
            if not self.producto_combo.get():
                self.producto_combo['values'] = self.productos_completos
    
    def cargar_ventas(self):
        """Cargar ventas en la tabla"""
        try:
            ventas = VentaModel.obtener_recientes()
            
            # Limpiar tabla
            for item in self.ventas_tree.get_children():
                self.ventas_tree.delete(item)
            
            # Insertar ventas
            for venta in ventas:
                fecha_formateada = venta[2].strftime("%Y-%m-%d %H:%M")
                self.ventas_tree.insert('', 'end', values=(
                    venta[0], venta[1], fecha_formateada, f"${venta[3]:.2f}", venta[4]
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas: {str(e)}")
    
    def ordenar_tabla(self, col):
        """Ordenar tabla por columna"""
        # Solo permitir ordenamiento en columnas visibles
        if col == 'ID':
            return
            
        self.sort_column, self.sort_reverse = TableSorter.sort_treeview(
            self.ventas_tree, col, self.sort_column, self.sort_reverse, 
            numeric_columns=['Total']
        )
        
        TableSorter.update_header_indicators(self.ventas_tree, col, self.sort_reverse, self.all_columns_ventas)