"""
Vista para la pestaña de clientes
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.cliente import ClienteModel
from utils.validators import Validators
from utils.table_sorter import TableSorter

class ClientesTab:
    """Clase para manejar la pestaña de clientes"""
    
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        
        # Variables para control de ordenamiento
        self.sort_column = None
        self.sort_reverse = False
        
        self.setup_ui()
        self.cargar_clientes()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame superior para formulario
        form_frame = tk.Frame(self.frame, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Gestión de Clientes", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Campos del formulario
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(pady=10)
        
        tk.Label(fields_frame, text="Nombre:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nombre_entry = tk.Entry(fields_frame, width=25)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Apellido:", bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.apellido_entry = tk.Entry(fields_frame, width=25)
        self.apellido_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Teléfono:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.telefono_entry = tk.Entry(fields_frame, width=25)
        self.telefono_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Email:", bg='white').grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.email_entry = tk.Entry(fields_frame, width=25)
        self.email_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(fields_frame, text="Dirección:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.direccion_entry = tk.Entry(fields_frame, width=55)
        self.direccion_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        
        # Botones
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="Agregar", command=self.agregar_cliente, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Actualizar", command=self.actualizar_cliente, bg='#3498db', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Eliminar", command=self.eliminar_cliente, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Limpiar", command=self.limpiar_campos, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        # Tabla de clientes
        table_frame = tk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columnas completas (incluye ID para funcionalidad interna)
        self.all_columns = ('ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Puntos')
        
        self.tree = ttk.Treeview(table_frame, columns=self.all_columns, show='headings', height=15)
        
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
        
        self.tree.bind('<ButtonRelease-1>', self.seleccionar_cliente)
    
    def agregar_cliente(self):
        """Agregar nuevo cliente"""
        errors = Validators.validar_cliente(
            self.nombre_entry.get(), 
            self.apellido_entry.get(), 
            self.email_entry.get()
        )
        if errors:
            messagebox.showerror("Error de Validación", "\n".join(errors))
            return
        
        try:
            ClienteModel.crear(
                self.nombre_entry.get(),
                self.apellido_entry.get(),
                self.telefono_entry.get(),
                self.email_entry.get(),
                self.direccion_entry.get()
            )
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            self.limpiar_campos()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar cliente: {str(e)}")
    
    def actualizar_cliente(self):
        """Actualizar cliente seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return
        
        errors = Validators.validar_cliente(
            self.nombre_entry.get(), 
            self.apellido_entry.get(), 
            self.email_entry.get()
        )
        if errors:
            messagebox.showerror("Error de Validación", "\n".join(errors))
            return
        
        item = self.tree.item(selected[0])
        cliente_id = item['values'][0]
        
        try:
            ClienteModel.actualizar(
                cliente_id,
                self.nombre_entry.get(),
                self.apellido_entry.get(),
                self.telefono_entry.get(),
                self.email_entry.get(),
                self.direccion_entry.get()
            )
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self.limpiar_campos()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")
    
    def eliminar_cliente(self):
        """Eliminar cliente seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        item = self.tree.item(selected[0])
        cliente_nombre = f"{item['values'][1]} {item['values'][2]}"
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el cliente '{cliente_nombre}'?"):
            cliente_id = item['values'][0]
            
            try:
                ClienteModel.eliminar(cliente_id)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargar_clientes()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
    
    def limpiar_campos(self):
        """Limpiar campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)
    
    def seleccionar_cliente(self, event):
        """Cargar datos del cliente seleccionado en el formulario"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.limpiar_campos()
            self.nombre_entry.insert(0, values[1])
            self.apellido_entry.insert(0, values[2])
            self.telefono_entry.insert(0, values[3])
            self.email_entry.insert(0, values[4])
            
            # Obtener dirección completa de la base de datos
            try:
                direccion = ClienteModel.obtener_direccion(values[0])
                if direccion:
                    self.direccion_entry.insert(0, direccion)
            except Exception:
                pass  # Si hay error, simplemente no cargar la dirección
    
    def cargar_clientes(self):
        """Cargar clientes en la tabla"""
        try:
            clientes = ClienteModel.obtener_todos()
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar clientes
            for cliente in clientes:
                self.tree.insert('', 'end', values=cliente)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
    
    def ordenar_tabla(self, col):
        """Ordenar tabla por columna"""
        # Solo permitir ordenamiento en columnas visibles
        if col == 'ID':
            return
            
        self.sort_column, self.sort_reverse = TableSorter.sort_treeview(
            self.tree, col, self.sort_column, self.sort_reverse, 
            numeric_columns=['Puntos']
        )
        
        TableSorter.update_header_indicators(self.tree, col, self.sort_reverse, self.all_columns)