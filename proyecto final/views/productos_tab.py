"""
Vista para la pestaña de productos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.producto import ProductoModel
from utils.validators import Validators
from utils.table_sorter import TableSorter

class ProductosTab:
    """Clase para manejar la pestaña de productos"""
    
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        
        # Variables para control de ordenamiento
        self.sort_column = None
        self.sort_reverse = False
        
        self.setup_ui()
        self.cargar_productos()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame superior para formulario
        form_frame = tk.Frame(self.frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Gestión de Productos", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Campos del formulario
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(pady=10)
        
        tk.Label(fields_frame, text="Nombre:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nombre_entry = tk.Entry(fields_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Descripción:", bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.descripcion_entry = tk.Entry(fields_frame, width=30)
        self.descripcion_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Precio:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.precio_entry = tk.Entry(fields_frame, width=30)
        self.precio_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Categoría:", bg='white').grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.categoria_combo = ttk.Combobox(fields_frame, width=27, values=['Dulces', 'Chocolates', 'Bebidas', 'Snacks', 'Otros'])
        self.categoria_combo.grid(row=1, column=3, padx=5, pady=5)
        
        # Botones
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="Agregar", command=self.agregar_producto, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Actualizar", command=self.actualizar_producto, bg='#3498db', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Eliminar", command=self.eliminar_producto, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Limpiar", command=self.limpiar_campos, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        # Tabla de productos
        table_frame = tk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columnas completas (incluye ID para funcionalidad interna)
        self.all_columns = ('ID', 'Nombre', 'Descripción', 'Precio', 'Categoría')
        # Columnas visibles (sin ID)
        visible_columns = ('Nombre', 'Descripción', 'Precio', 'Categoría')
        
        self.tree = ttk.Treeview(table_frame, columns=self.all_columns, show='headings', height=15)
        
        # Configurar solo las columnas visibles
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
        
        self.tree.bind('<ButtonRelease-1>', self.seleccionar_producto)
    
    def agregar_producto(self):
        """Agregar nuevo producto"""
        errors = Validators.validar_producto(self.nombre_entry.get(), self.precio_entry.get())
        if errors:
            messagebox.showerror("Error de Validación", "\n".join(errors))
            return
        
        try:
            ProductoModel.crear(
                self.nombre_entry.get(),
                self.descripcion_entry.get(),
                float(self.precio_entry.get()),
                self.categoria_combo.get()
            )
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_campos()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def actualizar_producto(self):
        """Actualizar producto seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar")
            return
        
        errors = Validators.validar_producto(self.nombre_entry.get(), self.precio_entry.get())
        if errors:
            messagebox.showerror("Error de Validación", "\n".join(errors))
            return
        
        item = self.tree.item(selected[0])
        producto_id = item['values'][0]
        
        try:
            ProductoModel.actualizar(
                producto_id,
                self.nombre_entry.get(),
                self.descripcion_entry.get(),
                float(self.precio_entry.get()),
                self.categoria_combo.get()
            )
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.limpiar_campos()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {str(e)}")
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado en cascada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        item = self.tree.item(selected[0])
        producto_nombre = item['values'][1]
        producto_id = item['values'][0]
        
        try:
            ventas_count, inventario_count = ProductoModel.obtener_info_eliminacion(producto_id)
            
            # Mostrar advertencia detallada
            mensaje_confirmacion = f"¿Está seguro de eliminar COMPLETAMENTE el producto '{producto_nombre}'?\n\n"
            mensaje_confirmacion += "ELIMINACIÓN EN CASCADA:\n"
            mensaje_confirmacion += f"• Producto: {producto_nombre}\n"
            
            if ventas_count > 0:
                mensaje_confirmacion += f"• {ventas_count} registro(s) de ventas\n"
            
            if inventario_count > 0:
                mensaje_confirmacion += f"• {inventario_count} registro(s) de inventario\n"
            
            mensaje_confirmacion += "\ESTA ACCIÓN NO SE PUEDE DESHACER\n"
            mensaje_confirmacion += "Se eliminará TODO el historial relacionado con este producto."
            
            if messagebox.askyesno("ELIMINACIÓN EN CASCADA", mensaje_confirmacion):
                ProductoModel.eliminar_cascada(producto_id)
                
                mensaje_exito = f"Producto '{producto_nombre}' eliminado completamente:\n"
                if ventas_count > 0:
                    mensaje_exito += f"{ventas_count} registro(s) de ventas eliminados\n"
                if inventario_count > 0:
                    mensaje_exito += f"{inventario_count} registro(s) de inventario eliminados\n"
                mensaje_exito += "Producto eliminado de la base de datos"
                
                messagebox.showinfo("Eliminación Exitosa", mensaje_exito)
                self.cargar_productos()
                self.limpiar_campos()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
    

    
    def limpiar_campos(self):
        """Limpiar campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.categoria_combo.set('')
    
    def seleccionar_producto(self, event):
        """Cargar datos del producto seleccionado en el formulario"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.limpiar_campos()
            # Los índices siguen siendo los mismos porque mantenemos todas las columnas internamente
            self.nombre_entry.insert(0, values[1])  # Nombre
            self.descripcion_entry.insert(0, values[2])  # Descripción
            self.precio_entry.insert(0, values[3])  # Precio
            self.categoria_combo.set(values[4])  # Categoría
    
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        try:
            productos = ProductoModel.obtener_todos()
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar productos
            for producto in productos:
                self.tree.insert('', 'end', values=producto)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def ordenar_tabla(self, col):
        """Ordenar tabla por columna"""
        # Solo permitir ordenamiento en columnas visibles
        if col == 'ID':
            return
            
        self.sort_column, self.sort_reverse = TableSorter.sort_treeview(
            self.tree, col, self.sort_column, self.sort_reverse, 
            numeric_columns=['Precio']
        )
        
        TableSorter.update_header_indicators(self.tree, col, self.sort_reverse, self.all_columns)