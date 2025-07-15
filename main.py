import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime
import json
from config import DB_CONFIG, APP_CONFIG

class DulceriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(APP_CONFIG['geometry'])
        self.root.configure(bg='#f0f0f0')
        
        # Configuración de la base de datos
        self.db_config = DB_CONFIG
        
        self.setup_ui()
        
    def setup_ui(self):
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
        self.create_productos_tab()
        self.create_clientes_tab()
        self.create_ventas_tab()
        self.create_inventario_tab()
        self.create_reportes_tab()
        
    def get_db_connection(self):
        """Establece conexión con la base de datos"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")
            return None

    def create_productos_tab(self):
        """Pestaña de gestión de productos"""
        productos_frame = ttk.Frame(self.notebook)
        self.notebook.add(productos_frame, text="Productos")
        
        # Frame superior para formulario
        form_frame = tk.Frame(productos_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Gestión de Productos", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Campos del formulario
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(pady=10)
        
        tk.Label(fields_frame, text="Nombre:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.producto_nombre = tk.Entry(fields_frame, width=30)
        self.producto_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Descripción:", bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.producto_descripcion = tk.Entry(fields_frame, width=30)
        self.producto_descripcion.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Precio:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.producto_precio = tk.Entry(fields_frame, width=30)
        self.producto_precio.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Categoría:", bg='white').grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.producto_categoria = ttk.Combobox(fields_frame, width=27, values=['Dulces', 'Chocolates', 'Bebidas', 'Snacks', 'Otros'])
        self.producto_categoria.grid(row=1, column=3, padx=5, pady=5)
        
        # Botones
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="Agregar", command=self.agregar_producto, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Actualizar", command=self.actualizar_producto, bg='#3498db', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Eliminar", command=self.eliminar_producto, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Limpiar", command=self.limpiar_productos, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        # Tabla de productos
        table_frame = tk.Frame(productos_frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombre', 'Descripción', 'Precio', 'Categoría', 'Activo')
        self.productos_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.productos_tree.heading(col, text=col)
            self.productos_tree.column(col, width=120)
        
        scrollbar_productos = ttk.Scrollbar(table_frame, orient='vertical', command=self.productos_tree.yview)
        self.productos_tree.configure(yscrollcommand=scrollbar_productos.set)
        
        self.productos_tree.pack(side='left', fill='both', expand=True)
        scrollbar_productos.pack(side='right', fill='y')
        
        self.productos_tree.bind('<ButtonRelease-1>', self.seleccionar_producto)
        
        # Cargar productos al iniciar
        self.cargar_productos()
    
    def agregar_producto(self):
        """Agregar nuevo producto"""
        if not self.validar_producto():
            return
            
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = """INSERT INTO Productos (nombre, descripcion, precio, categoria) 
                      VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (
                self.producto_nombre.get(),
                self.producto_descripcion.get(),
                float(self.producto_precio.get()),
                self.producto_categoria.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_productos()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
        finally:
            conn.close()
    
    def actualizar_producto(self):
        """Actualizar producto seleccionado"""
        selected = self.productos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar")
            return
            
        if not self.validar_producto():
            return
            
        item = self.productos_tree.item(selected[0])
        producto_id = item['values'][0]
        
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = """UPDATE Productos SET nombre=%s, descripcion=%s, precio=%s, categoria=%s 
                      WHERE id_producto=%s"""
            cursor.execute(query, (
                self.producto_nombre.get(),
                self.producto_descripcion.get(),
                float(self.producto_precio.get()),
                self.producto_categoria.get(),
                producto_id
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.limpiar_productos()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {str(e)}")
        finally:
            conn.close()
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        selected = self.productos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
            
        item = self.productos_tree.item(selected[0])
        producto_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto '{producto_nombre}'?\n\nEsta acción no se puede deshacer."):
            producto_id = item['values'][0]
            
            conn = self.get_db_connection()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                
                # Verificar si el producto tiene ventas asociadas
                cursor.execute("SELECT COUNT(*) FROM Detalle_Venta WHERE id_producto=%s", (producto_id,))
                ventas_count = cursor.fetchone()[0]
                
                if ventas_count > 0:
                    # Si tiene ventas, solo desactivar para mantener integridad referencial
                    if messagebox.askyesno("Producto con Ventas", 
                                         f"Este producto tiene {ventas_count} venta(s) registrada(s).\n\n"
                                         "¿Desea desactivarlo en lugar de eliminarlo?\n"
                                         "(Recomendado para mantener el historial de ventas)"):
                        cursor.execute("UPDATE Productos SET activo=FALSE WHERE id_producto=%s", (producto_id,))
                        conn.commit()
                        messagebox.showinfo("Éxito", "Producto desactivado correctamente")
                    else:
                        return
                else:
                    # Si no tiene ventas, eliminar completamente
                    # Primero eliminar del inventario si existe
                    cursor.execute("DELETE FROM Inventario WHERE id_producto=%s", (producto_id,))
                    # Luego eliminar el producto
                    cursor.execute("DELETE FROM Productos WHERE id_producto=%s", (producto_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Producto eliminado completamente")
                
                self.cargar_productos()
                self.limpiar_productos()
                
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
            finally:
                conn.close()
    
    def validar_producto(self):
        """Validar campos del producto"""
        if not self.producto_nombre.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return False
        try:
            float(self.producto_precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
            return False
        return True
    
    def limpiar_productos(self):
        """Limpiar campos del formulario de productos"""
        self.producto_nombre.delete(0, tk.END)
        self.producto_descripcion.delete(0, tk.END)
        self.producto_precio.delete(0, tk.END)
        self.producto_categoria.set('')
    
    def seleccionar_producto(self, event):
        """Cargar datos del producto seleccionado en el formulario"""
        selected = self.productos_tree.selection()
        if selected:
            item = self.productos_tree.item(selected[0])
            values = item['values']
            
            self.limpiar_productos()
            self.producto_nombre.insert(0, values[1])
            self.producto_descripcion.insert(0, values[2])
            self.producto_precio.insert(0, values[3])
            self.producto_categoria.set(values[4])
    
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_producto, nombre, descripcion, precio, categoria, activo FROM Productos ORDER BY nombre")
            productos = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.productos_tree.get_children():
                self.productos_tree.delete(item)
            
            # Insertar productos
            for producto in productos:
                self.productos_tree.insert('', 'end', values=producto)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
        finally:
            conn.close()

    def create_clientes_tab(self):
        """Pestaña de gestión de clientes"""
        clientes_frame = ttk.Frame(self.notebook)
        self.notebook.add(clientes_frame, text="Clientes")
        
        # Frame superior para formulario
        form_frame = tk.Frame(clientes_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Gestión de Clientes", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Campos del formulario
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(pady=10)
        
        tk.Label(fields_frame, text="Nombre:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.cliente_nombre = tk.Entry(fields_frame, width=25)
        self.cliente_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Apellido:", bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.cliente_apellido = tk.Entry(fields_frame, width=25)
        self.cliente_apellido.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Teléfono:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.cliente_telefono = tk.Entry(fields_frame, width=25)
        self.cliente_telefono.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Email:", bg='white').grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.cliente_email = tk.Entry(fields_frame, width=25)
        self.cliente_email.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Dirección:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.cliente_direccion = tk.Entry(fields_frame, width=55)
        self.cliente_direccion.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        
        # Botones
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="Agregar", command=self.agregar_cliente, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Actualizar", command=self.actualizar_cliente, bg='#3498db', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Eliminar", command=self.eliminar_cliente, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Limpiar", command=self.limpiar_clientes, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        # Tabla de clientes
        table_frame = tk.Frame(clientes_frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Puntos')
        self.clientes_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.clientes_tree.heading(col, text=col)
            self.clientes_tree.column(col, width=120)
        
        scrollbar_clientes = ttk.Scrollbar(table_frame, orient='vertical', command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar_clientes.set)
        
        self.clientes_tree.pack(side='left', fill='both', expand=True)
        scrollbar_clientes.pack(side='right', fill='y')
        
        self.clientes_tree.bind('<ButtonRelease-1>', self.seleccionar_cliente)
        
        # Cargar clientes al iniciar
        self.cargar_clientes()
    
    def agregar_cliente(self):
        """Agregar nuevo cliente"""
        if not self.validar_cliente():
            return
            
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = """INSERT INTO Clientes (nombre, apellido, telefono, email, direccion) 
                      VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                self.cliente_nombre.get(),
                self.cliente_apellido.get(),
                self.cliente_telefono.get(),
                self.cliente_email.get(),
                self.cliente_direccion.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            self.limpiar_clientes()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar cliente: {str(e)}")
        finally:
            conn.close()
    
    def actualizar_cliente(self):
        """Actualizar cliente seleccionado"""
        selected = self.clientes_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return
            
        if not self.validar_cliente():
            return
            
        item = self.clientes_tree.item(selected[0])
        cliente_id = item['values'][0]
        
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = """UPDATE Clientes SET nombre=%s, apellido=%s, telefono=%s, email=%s, direccion=%s 
                      WHERE id_cliente=%s"""
            cursor.execute(query, (
                self.cliente_nombre.get(),
                self.cliente_apellido.get(),
                self.cliente_telefono.get(),
                self.cliente_email.get(),
                self.cliente_direccion.get(),
                cliente_id
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self.limpiar_clientes()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")
        finally:
            conn.close()
    
    def eliminar_cliente(self):
        """Eliminar cliente seleccionado"""
        selected = self.clientes_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            item = self.clientes_tree.item(selected[0])
            cliente_id = item['values'][0]
            
            conn = self.get_db_connection()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Clientes WHERE id_cliente=%s", (cliente_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
            finally:
                conn.close()
    
    def validar_cliente(self):
        """Validar campos del cliente"""
        if not self.cliente_nombre.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return False
        if not self.cliente_apellido.get().strip():
            messagebox.showerror("Error", "El apellido es obligatorio")
            return False
        return True
    
    def limpiar_clientes(self):
        """Limpiar campos del formulario de clientes"""
        self.cliente_nombre.delete(0, tk.END)
        self.cliente_apellido.delete(0, tk.END)
        self.cliente_telefono.delete(0, tk.END)
        self.cliente_email.delete(0, tk.END)
        self.cliente_direccion.delete(0, tk.END)
    
    def seleccionar_cliente(self, event):
        """Cargar datos del cliente seleccionado en el formulario"""
        selected = self.clientes_tree.selection()
        if selected:
            item = self.clientes_tree.item(selected[0])
            values = item['values']
            
            self.limpiar_clientes()
            self.cliente_nombre.insert(0, values[1])
            self.cliente_apellido.insert(0, values[2])
            self.cliente_telefono.insert(0, values[3])
            self.cliente_email.insert(0, values[4])
            
            # Obtener dirección completa de la base de datos
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT direccion FROM Clientes WHERE id_cliente=%s", (values[0],))
                    result = cursor.fetchone()
                    if result and result[0]:
                        self.cliente_direccion.insert(0, result[0])
                except Exception as e:
                    pass
                finally:
                    conn.close()
    
    def cargar_clientes(self):
        """Cargar clientes en la tabla"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nombre, apellido, telefono, email, puntos_fidelidad FROM Clientes ORDER BY apellido, nombre")
            clientes = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.clientes_tree.get_children():
                self.clientes_tree.delete(item)
            
            # Insertar clientes
            for cliente in clientes:
                self.clientes_tree.insert('', 'end', values=cliente)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
        finally:
            conn.close()

    def create_ventas_tab(self):
        """Pestaña de gestión de ventas"""
        ventas_frame = ttk.Frame(self.notebook)
        self.notebook.add(ventas_frame, text="Ventas")
        
        # Frame superior para nueva venta
        form_frame = tk.Frame(ventas_frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Nueva Venta", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Selección de cliente
        cliente_frame = tk.Frame(form_frame, bg='white')
        cliente_frame.pack(pady=5)
        
        tk.Label(cliente_frame, text="Cliente:", bg='white').pack(side='left', padx=5)
        self.venta_cliente = ttk.Combobox(cliente_frame, width=40, state='readonly')
        self.venta_cliente.pack(side='left', padx=5)
        
        tk.Label(cliente_frame, text="Método de Pago:", bg='white').pack(side='left', padx=5)
        self.venta_metodo_pago = ttk.Combobox(cliente_frame, width=20, values=['Efectivo', 'Tarjeta', 'Transferencia'])
        self.venta_metodo_pago.pack(side='left', padx=5)
        
        # Selección de productos
        productos_frame = tk.Frame(form_frame, bg='white')
        productos_frame.pack(pady=10, fill='x')
        
        tk.Label(productos_frame, text="Agregar Producto:", bg='white').pack(anchor='w', padx=5)
        
        producto_select_frame = tk.Frame(productos_frame, bg='white')
        producto_select_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(producto_select_frame, text="Producto:", bg='white').pack(side='left')
        self.venta_producto = ttk.Combobox(producto_select_frame, width=30, state='readonly')
        self.venta_producto.pack(side='left', padx=5)
        
        tk.Label(producto_select_frame, text="Cantidad:", bg='white').pack(side='left', padx=5)
        self.venta_cantidad = tk.Entry(producto_select_frame, width=10)
        self.venta_cantidad.pack(side='left', padx=5)
        
        tk.Button(producto_select_frame, text="Agregar", command=self.agregar_producto_venta, 
                 bg='#27ae60', fg='white').pack(side='left', padx=5)
        
        # Lista de productos en la venta
        self.productos_venta = []
        
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
        ventas_realizadas_frame = tk.Frame(ventas_frame)
        ventas_realizadas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(ventas_realizadas_frame, text="Ventas Realizadas", font=('Arial', 14, 'bold')).pack(pady=5)
        
        columns_ventas = ('ID', 'Cliente', 'Fecha', 'Total', 'Método Pago')
        self.ventas_tree = ttk.Treeview(ventas_realizadas_frame, columns=columns_ventas, show='headings', height=10)
        
        for col in columns_ventas:
            self.ventas_tree.heading(col, text=col)
            self.ventas_tree.column(col, width=120)
        
        scrollbar_ventas = ttk.Scrollbar(ventas_realizadas_frame, orient='vertical', command=self.ventas_tree.yview)
        self.ventas_tree.configure(yscrollcommand=scrollbar_ventas.set)
        
        self.ventas_tree.pack(side='left', fill='both', expand=True)
        scrollbar_ventas.pack(side='right', fill='y')
        
        # Cargar datos iniciales
        self.cargar_clientes_combo()
        self.cargar_productos_combo()
        self.cargar_ventas()
    
    def cargar_clientes_combo(self):
        """Cargar clientes en el combobox"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nombre, apellido FROM Clientes ORDER BY apellido, nombre")
            clientes = cursor.fetchall()
            
            cliente_values = [f"{cliente[0]} - {cliente[1]} {cliente[2]}" for cliente in clientes]
            self.venta_cliente['values'] = cliente_values
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
        finally:
            conn.close()
    
    def cargar_productos_combo(self):
        """Cargar productos en el combobox"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_producto, nombre, precio FROM Productos WHERE activo=TRUE ORDER BY nombre")
            productos = cursor.fetchall()
            
            producto_values = [f"{producto[0]} - {producto[1]} (${producto[2]})" for producto in productos]
            self.venta_producto['values'] = producto_values
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
        finally:
            conn.close()
    
    def agregar_producto_venta(self):
        """Agregar producto a la venta actual"""
        if not self.venta_producto.get() or not self.venta_cantidad.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto y especifique la cantidad")
            return
        
        try:
            cantidad = int(self.venta_cantidad.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo")
            return
        
        # Extraer información del producto
        producto_info = self.venta_producto.get()
        producto_id = int(producto_info.split(' - ')[0])
        
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, precio FROM Productos WHERE id_producto=%s", (producto_id,))
            producto = cursor.fetchone()
            
            if producto:
                nombre, precio = producto
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
                self.venta_producto.set('')
                self.venta_cantidad.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
        finally:
            conn.close()
    
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
        if not self.venta_cliente.get():
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return
        
        if not self.venta_metodo_pago.get():
            messagebox.showwarning("Advertencia", "Seleccione un método de pago")
            return
        
        if not self.productos_venta:
            messagebox.showwarning("Advertencia", "Agregue al menos un producto a la venta")
            return
        
        # Extraer ID del cliente
        cliente_info = self.venta_cliente.get()
        cliente_id = int(cliente_info.split(' - ')[0])
        
        # Calcular total
        total = sum(producto['subtotal'] for producto in self.productos_venta)
        
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            
            # Insertar venta
            cursor.execute("""INSERT INTO Ventas (id_cliente, total, metodo_pago) 
                             VALUES (%s, %s, %s) RETURNING id_venta""",
                          (cliente_id, total, self.venta_metodo_pago.get()))
            venta_id = cursor.fetchone()[0]
            
            # Insertar detalles de venta
            for producto in self.productos_venta:
                cursor.execute("""INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario) 
                                 VALUES (%s, %s, %s, %s)""",
                              (venta_id, producto['id'], producto['cantidad'], producto['precio']))
            
            conn.commit()
            messagebox.showinfo("Éxito", f"Venta procesada correctamente. ID: {venta_id}")
            
            # Limpiar venta
            self.limpiar_venta()
            self.cargar_ventas()
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error al procesar venta: {str(e)}")
        finally:
            conn.close()
    
    def limpiar_venta(self):
        """Limpiar formulario de venta"""
        self.venta_cliente.set('')
        self.venta_metodo_pago.set('')
        self.venta_producto.set('')
        self.venta_cantidad.delete(0, tk.END)
        self.productos_venta = []
        self.actualizar_tabla_venta()
    
    def cargar_ventas(self):
        """Cargar ventas en la tabla"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT v.id_venta, CONCAT(c.nombre, ' ', c.apellido), 
                                    v.fecha_venta, v.total, v.metodo_pago
                             FROM Ventas v 
                             JOIN Clientes c ON v.id_cliente = c.id_cliente 
                             ORDER BY v.fecha_venta DESC LIMIT 50""")
            ventas = cursor.fetchall()
            
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
        finally:
            conn.close()

    def create_inventario_tab(self):
        """Pestaña de gestión de inventario"""
        inventario_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventario_frame, text="Inventario")
        
        # Frame superior para controles
        control_frame = tk.Frame(inventario_frame, bg='white', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="Gestión de Inventario", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Controles de reposición
        reposicion_frame = tk.Frame(control_frame, bg='white')
        reposicion_frame.pack(pady=10)
        
        tk.Label(reposicion_frame, text="Producto:", bg='white').pack(side='left', padx=5)
        self.inventario_producto = ttk.Combobox(reposicion_frame, width=30, state='readonly')
        self.inventario_producto.pack(side='left', padx=5)
        
        tk.Label(reposicion_frame, text="Cantidad a agregar:", bg='white').pack(side='left', padx=5)
        self.inventario_cantidad = tk.Entry(reposicion_frame, width=10)
        self.inventario_cantidad.pack(side='left', padx=5)
        
        tk.Label(reposicion_frame, text="Ubicación:", bg='white').pack(side='left', padx=5)
        self.inventario_ubicacion = tk.Entry(reposicion_frame, width=15)
        self.inventario_ubicacion.pack(side='left', padx=5)
        
        tk.Button(reposicion_frame, text="Reponer Stock", command=self.reponer_inventario, 
                 bg='#27ae60', fg='white').pack(side='left', padx=10)
        
        # Tabla de inventario
        table_frame = tk.Frame(inventario_frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Producto', 'Cantidad', 'Ubicación', 'Última Actualización')
        self.inventario_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.inventario_tree.heading(col, text=col)
            self.inventario_tree.column(col, width=150)
        
        scrollbar_inventario = ttk.Scrollbar(table_frame, orient='vertical', command=self.inventario_tree.yview)
        self.inventario_tree.configure(yscrollcommand=scrollbar_inventario.set)
        
        self.inventario_tree.pack(side='left', fill='both', expand=True)
        scrollbar_inventario.pack(side='right', fill='y')
        
        # Cargar datos
        self.cargar_productos_inventario()
        self.cargar_inventario()
    
    def cargar_productos_inventario(self):
        """Cargar productos para el inventario"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_producto, nombre FROM Productos WHERE activo=TRUE ORDER BY nombre")
            productos = cursor.fetchall()
            
            producto_values = [f"{producto[0]} - {producto[1]}" for producto in productos]
            self.inventario_producto['values'] = producto_values
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
        finally:
            conn.close()
    
    def reponer_inventario(self):
        """Reponer stock de inventario"""
        if not self.inventario_producto.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        try:
            cantidad = int(self.inventario_cantidad.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo")
            return
        
        # Extraer ID del producto
        producto_info = self.inventario_producto.get()
        producto_id = int(producto_info.split(' - ')[0])
        ubicacion = self.inventario_ubicacion.get() or 'Sin especificar'
        
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            
            # Verificar si ya existe registro de inventario
            cursor.execute("SELECT id_inventario, cantidad FROM Inventario WHERE id_producto=%s", (producto_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Actualizar cantidad existente
                cursor.execute("""UPDATE Inventario SET cantidad = cantidad + %s, 
                                 fecha_actualizacion = CURRENT_TIMESTAMP, ubicacion = %s 
                                 WHERE id_producto = %s""",
                              (cantidad, ubicacion, producto_id))
            else:
                # Crear nuevo registro
                cursor.execute("""INSERT INTO Inventario (id_producto, cantidad, ubicacion) 
                                 VALUES (%s, %s, %s)""",
                              (producto_id, cantidad, ubicacion))
            
            conn.commit()
            messagebox.showinfo("Éxito", f"Inventario actualizado: +{cantidad} unidades")
            
            # Limpiar campos
            self.inventario_producto.set('')
            self.inventario_cantidad.delete(0, tk.END)
            self.inventario_ubicacion.delete(0, tk.END)
            
            # Recargar inventario
            self.cargar_inventario()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al reponer inventario: {str(e)}")
        finally:
            conn.close()
    
    def cargar_inventario(self):
        """Cargar inventario en la tabla"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT i.id_inventario, p.nombre, i.cantidad, i.ubicacion, i.fecha_actualizacion
                             FROM Inventario i 
                             JOIN Productos p ON i.id_producto = p.id_producto 
                             ORDER BY p.nombre""")
            inventario = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.inventario_tree.get_children():
                self.inventario_tree.delete(item)
            
            # Insertar inventario
            for item in inventario:
                fecha_formateada = item[4].strftime("%Y-%m-%d %H:%M")
                self.inventario_tree.insert('', 'end', values=(
                    item[0], item[1], item[2], item[3] or 'Sin especificar', fecha_formateada
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inventario: {str(e)}")
        finally:
            conn.close()
    
    def create_reportes_tab(self):
        """Pestaña de reportes"""
        reportes_frame = ttk.Frame(self.notebook)
        self.notebook.add(reportes_frame, text="Reportes")
        
        # Frame superior para controles
        control_frame = tk.Frame(reportes_frame, bg='white', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="Reportes y Estadísticas", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Botones de reportes
        buttons_frame = tk.Frame(control_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="Productos Más Vendidos", command=self.reporte_productos_vendidos, 
                 bg='#3498db', fg='white', width=20).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Ventas por Cliente", command=self.reporte_ventas_cliente, 
                 bg='#9b59b6', fg='white', width=20).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Stock Bajo", command=self.reporte_stock_bajo, 
                 bg='#e67e22', fg='white', width=20).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Ventas del Mes", command=self.reporte_ventas_mes, 
                 bg='#1abc9c', fg='white', width=20).pack(side='left', padx=5)
        
        # Área de resultados
        self.reportes_text = tk.Text(reportes_frame, height=25, font=('Courier', 10))
        self.reportes_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar_reportes = ttk.Scrollbar(reportes_frame, orient='vertical', command=self.reportes_text.yview)
        self.reportes_text.configure(yscrollcommand=scrollbar_reportes.set)
        scrollbar_reportes.pack(side='right', fill='y')
    
    def reporte_productos_vendidos(self):
        """Generar reporte de productos más vendidos"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nombre, SUM(dv.cantidad) as total_vendido, 
                       SUM(dv.subtotal) as ingresos_totales
                FROM Detalle_Venta dv
                JOIN Productos p ON dv.id_producto = p.id_producto
                GROUP BY p.id_producto, p.nombre
                ORDER BY total_vendido DESC
                LIMIT 10
            """)
            resultados = cursor.fetchall()
            
            reporte = "PRODUCTOS MÁS VENDIDOS\n"
            reporte += "=" * 60 + "\n\n"
            reporte += f"{'Producto':<30} {'Cantidad':<10} {'Ingresos':<15}\n"
            reporte += "-" * 60 + "\n"
            
            for producto, cantidad, ingresos in resultados:
                reporte += f"{producto:<30} {cantidad:<10} ${ingresos:<14.2f}\n"
            
            self.reportes_text.delete(1.0, tk.END)
            self.reportes_text.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
        finally:
            conn.close()
    
    def reporte_ventas_cliente(self):
        """Generar reporte de ventas por cliente"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT CONCAT(c.nombre, ' ', c.apellido) as cliente, 
                       COUNT(v.id_venta) as num_compras,
                       SUM(v.total) as total_gastado,
                       c.puntos_fidelidad
                FROM Ventas v
                JOIN Clientes c ON v.id_cliente = c.id_cliente
                GROUP BY c.id_cliente, c.nombre, c.apellido, c.puntos_fidelidad
                ORDER BY total_gastado DESC
                LIMIT 15
            """)
            resultados = cursor.fetchall()
            
            reporte = "VENTAS POR CLIENTE\n"
            reporte += "=" * 80 + "\n\n"
            reporte += f"{'Cliente':<25} {'Compras':<8} {'Total Gastado':<15} {'Puntos':<8}\n"
            reporte += "-" * 80 + "\n"
            
            for cliente, compras, total, puntos in resultados:
                reporte += f"{cliente:<25} {compras:<8} ${total:<14.2f} {puntos:<8}\n"
            
            self.reportes_text.delete(1.0, tk.END)
            self.reportes_text.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
        finally:
            conn.close()
    
    def reporte_stock_bajo(self):
        """Generar reporte de productos con stock bajo"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nombre, i.cantidad, i.ubicacion, p.categoria
                FROM Inventario i
                JOIN Productos p ON i.id_producto = p.id_producto
                WHERE i.cantidad < 20
                ORDER BY i.cantidad ASC
            """)
            resultados = cursor.fetchall()
            
            reporte = "PRODUCTOS CON STOCK BAJO (< 20 unidades)\n"
            reporte += "=" * 70 + "\n\n"
            reporte += f"{'Producto':<25} {'Stock':<8} {'Ubicación':<15} {'Categoría':<15}\n"
            reporte += "-" * 70 + "\n"
            
            for producto, stock, ubicacion, categoria in resultados:
                reporte += f"{producto:<25} {stock:<8} {ubicacion or 'N/A':<15} {categoria or 'N/A':<15}\n"
            
            if not resultados:
                reporte += "¡Excelente! Todos los productos tienen stock suficiente.\n"
            
            self.reportes_text.delete(1.0, tk.END)
            self.reportes_text.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
        finally:
            conn.close()
    
    def reporte_ventas_mes(self):
        """Generar reporte de ventas del mes actual"""
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DATE(fecha_venta) as fecha, COUNT(*) as num_ventas, SUM(total) as total_dia
                FROM Ventas
                WHERE EXTRACT(MONTH FROM fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE)
                  AND EXTRACT(YEAR FROM fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE)
                GROUP BY DATE(fecha_venta)
                ORDER BY fecha DESC
            """)
            resultados = cursor.fetchall()
            
            # Totales del mes
            cursor.execute("""
                SELECT COUNT(*) as total_ventas, SUM(total) as ingresos_totales
                FROM Ventas
                WHERE EXTRACT(MONTH FROM fecha_venta) = EXTRACT(MONTH FROM CURRENT_DATE)
                  AND EXTRACT(YEAR FROM fecha_venta) = EXTRACT(YEAR FROM CURRENT_DATE)
            """)
            totales = cursor.fetchone()
            
            reporte = f"VENTAS DEL MES - {datetime.now().strftime('%B %Y').upper()}\n"
            reporte += "=" * 60 + "\n\n"
            reporte += f"RESUMEN DEL MES:\n"
            reporte += f"Total de ventas: {totales[0]}\n"
            reporte += f"Ingresos totales: ${totales[1]:.2f}\n\n"
            reporte += f"{'Fecha':<12} {'Ventas':<8} {'Total del Día':<15}\n"
            reporte += "-" * 40 + "\n"
            
            for fecha, ventas, total in resultados:
                reporte += f"{fecha:<12} {ventas:<8} ${total:<14.2f}\n"
            
            self.reportes_text.delete(1.0, tk.END)
            self.reportes_text.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DulceriaApp(root)
    root.mainloop()