"""
Vista para la pestaña de reportes
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.venta import VentaModel
from models.inventario import InventarioModel
from reports.pdf_generator import PDFGenerator

class ReportesTab:
    """Clase para manejar la pestaña de reportes"""
    
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        
        # Variables para almacenar el último reporte generado
        self.ultimo_reporte = None
        self.tipo_ultimo_reporte = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame superior para controles
        control_frame = tk.Frame(self.frame, bg='white', relief='raised', bd=2)
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
        
        # Frame para selector de fecha y botón de ventas
        ventas_frame = tk.Frame(control_frame, bg='white')
        ventas_frame.pack(pady=10)
        
        # Selectores de fecha
        tk.Label(ventas_frame, text="Reporte de Ventas:", font=('Arial', 12, 'bold'), bg='white').pack()
        
        fecha_selectors = tk.Frame(ventas_frame, bg='white')
        fecha_selectors.pack(pady=5)
        
        tk.Label(fecha_selectors, text="Mes:", bg='white').pack(side='left', padx=5)
        self.mes_combo = ttk.Combobox(fecha_selectors, width=12, values=[
            '1 - Enero', '2 - Febrero', '3 - Marzo', '4 - Abril', '5 - Mayo', '6 - Junio',
            '7 - Julio', '8 - Agosto', '9 - Septiembre', '10 - Octubre', '11 - Noviembre', '12 - Diciembre'
        ])
        self.mes_combo.pack(side='left', padx=5)
        
        tk.Label(fecha_selectors, text="Año:", bg='white').pack(side='left', padx=5)
        from datetime import datetime
        año_actual = datetime.now().year
        años = [str(año) for año in range(año_actual - 5, año_actual + 2)]
        self.año_combo = ttk.Combobox(fecha_selectors, width=8, values=años)
        self.año_combo.pack(side='left', padx=5)
        
        # Establecer valores por defecto (mes y año actual)
        mes_actual = datetime.now().month
        self.mes_combo.set(f'{mes_actual} - {["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes_actual]}')
        self.año_combo.set(str(año_actual))
        
        tk.Button(fecha_selectors, text="Generar Reporte", command=self.reporte_ventas_mes, 
                 bg='#1abc9c', fg='white', width=15).pack(side='left', padx=10)
        
        # Botón para exportar PDF
        export_frame = tk.Frame(control_frame, bg='white')
        export_frame.pack(pady=10)
        
        tk.Button(export_frame, text="Exportar Reporte a PDF", command=self.exportar_reporte_pdf, 
                 bg='#e74c3c', fg='white', width=25, font=('Arial', 10, 'bold')).pack()
        
        # Área de resultados
        self.text_area = tk.Text(self.frame, height=25, font=('Courier', 10))
        self.text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def reporte_productos_vendidos(self):
        """Generar reporte de productos más vendidos"""
        try:
            resultados = VentaModel.obtener_productos_mas_vendidos()
            
            # Guardar datos para exportación PDF
            self.ultimo_reporte = resultados
            self.tipo_ultimo_reporte = "productos_vendidos"
            
            reporte = "PRODUCTOS MÁS VENDIDOS\n"
            reporte += "=" * 60 + "\n\n"
            reporte += f"{'Producto':<30} {'Cantidad':<10} {'Ingresos':<15}\n"
            reporte += "-" * 60 + "\n"
            
            for producto, cantidad, ingresos in resultados:
                reporte += f"{producto:<30} {cantidad:<10} ${ingresos:<14.2f}\n"
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def reporte_ventas_cliente(self):
        """Generar reporte de ventas por cliente"""
        try:
            resultados = VentaModel.obtener_ventas_por_cliente()
            
            # Guardar datos para exportación PDF
            self.ultimo_reporte = resultados
            self.tipo_ultimo_reporte = "ventas_cliente"
            
            reporte = "VENTAS POR CLIENTE\n"
            reporte += "=" * 80 + "\n\n"
            reporte += f"{'Cliente':<25} {'Compras':<8} {'Total Gastado':<15} {'Puntos':<8}\n"
            reporte += "-" * 80 + "\n"
            
            for cliente, compras, total, puntos in resultados:
                reporte += f"{cliente:<25} {compras:<8} ${total:<14.2f} {puntos:<8}\n"
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def reporte_stock_bajo(self):
        """Generar reporte de productos con stock bajo"""
        try:
            resultados = InventarioModel.obtener_stock_bajo()
            
            # Guardar datos para exportación PDF
            self.ultimo_reporte = resultados
            self.tipo_ultimo_reporte = "stock_bajo"
            
            reporte = "PRODUCTOS CON STOCK BAJO (< 20 unidades)\n"
            reporte += "=" * 70 + "\n\n"
            reporte += f"{'Producto':<25} {'Stock':<8} {'Ubicación':<15} {'Categoría':<15}\n"
            reporte += "-" * 70 + "\n"
            
            for producto, stock, ubicacion, categoria in resultados:
                reporte += f"{producto:<25} {stock:<8} {ubicacion or 'N/A':<15} {categoria or 'N/A':<15}\n"
            
            if not resultados:
                reporte += "¡Excelente! Todos los productos tienen stock suficiente.\n"
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def reporte_ventas_mes(self):
        """Generar reporte de ventas del mes seleccionado"""
        try:
            # Obtener valores seleccionados
            mes_seleccionado = self.mes_combo.get()
            año_seleccionado = self.año_combo.get()
            
            if not mes_seleccionado or not año_seleccionado:
                messagebox.showwarning("Advertencia", "Por favor seleccione mes y año")
                return
            
            # Extraer número del mes (formato: "1 - Enero")
            mes_num = int(mes_seleccionado.split(' - ')[0])
            año_num = int(año_seleccionado)
            
            # Obtener información de debug primero
            debug_info = VentaModel.obtener_info_debug_ventas()
            
            # Obtener ventas del mes seleccionado
            ventas_diarias, totales = VentaModel.obtener_ventas_por_mes(mes_num, año_num)
            
            # Guardar datos para exportación PDF
            self.ultimo_reporte = {'resultados': ventas_diarias, 'totales': totales, 'mes': mes_num, 'año': año_num}
            self.tipo_ultimo_reporte = "ventas_mes"
            
            # Nombre del mes para mostrar
            nombres_meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            mes_nombre = nombres_meses[mes_num]
            
            reporte = f"VENTAS DEL MES - {mes_nombre.upper()} {año_num}\n"
            reporte += "=" * 60 + "\n\n"
            
            # Información de debug
            reporte += "INFORMACIÓN DEL SISTEMA:\n"
            reporte += f"Total de ventas en BD: {debug_info.get('total_ventas', 'N/A')}\n"
            reporte += f"Fecha actual del sistema: {debug_info.get('fecha_actual', 'N/A')}\n"
            reporte += f"Consultando: {mes_nombre} {año_num} (mes {mes_num})\n\n"
            
            # Mostrar ventas recientes para debug
            if 'ventas_recientes' in debug_info and debug_info['ventas_recientes']:
                reporte += "VENTAS RECIENTES (últimas 5):\n"
                for venta in debug_info['ventas_recientes']:
                    reporte += f"  {venta[0]} - ${venta[1]:.2f}\n"
                reporte += "\n"
            
            reporte += f"RESUMEN DEL MES:\n"
            
            # Manejar el caso donde totales puede ser una tupla o None
            if totales and len(totales) >= 2:
                total_ventas = totales[0] if totales[0] is not None else 0
                ingresos_totales = totales[1] if totales[1] is not None else 0.0
            else:
                total_ventas = 0
                ingresos_totales = 0.0
            
            reporte += f"Total de ventas del mes: {total_ventas}\n"
            reporte += f"Ingresos totales del mes: ${ingresos_totales:.2f}\n\n"
            
            if ventas_diarias and len(ventas_diarias) > 0:
                reporte += "DETALLE POR DÍAS:\n"
                reporte += f"{'Fecha':<12} {'Ventas':<8} {'Total del Día':<15}\n"
                reporte += "-" * 40 + "\n"
                
                for fecha, ventas, total in ventas_diarias:
                    fecha_str = str(fecha) if fecha else "N/A"
                    ventas_num = ventas if ventas is not None else 0
                    total_num = total if total is not None else 0.0
                    reporte += f"{fecha_str:<12} {ventas_num:<8} ${total_num:<14.2f}\n"
            else:
                reporte += f"No hay ventas registradas en {mes_nombre} {año_num}.\n"
                reporte += "\nSUGERENCIAS:\n"
                reporte += "- Verifique que haya ventas registradas en ese período\n"
                reporte += "- Revise las ventas recientes mostradas arriba\n"
                reporte += "- Pruebe con un mes/año diferente\n"
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, reporte)
            
        except Exception as e:
            error_msg = f"Error al generar reporte: {str(e)}\n\nDetalles técnicos: {type(e).__name__}"
            messagebox.showerror("Error", error_msg)
            
            # Mostrar error en el área de texto también
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, f"ERROR AL GENERAR REPORTE:\n{error_msg}")
    
    def exportar_reporte_pdf(self):
        """Exportar el último reporte generado a PDF"""
        if not self.ultimo_reporte or not self.tipo_ultimo_reporte:
            messagebox.showwarning("Advertencia", "Primero debe generar un reporte antes de exportarlo")
            return
        
        # Solicitar ubicación del archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar reporte como PDF"
        )
        
        if not archivo:
            return
        
        try:
            pdf_gen = PDFGenerator(archivo)
            
            # Generar contenido según el tipo de reporte
            if self.tipo_ultimo_reporte == "productos_vendidos":
                pdf_gen.generar_productos_vendidos(self.ultimo_reporte)
            elif self.tipo_ultimo_reporte == "ventas_cliente":
                pdf_gen.generar_ventas_cliente(self.ultimo_reporte)
            elif self.tipo_ultimo_reporte == "stock_bajo":
                pdf_gen.generar_stock_bajo(self.ultimo_reporte)
            elif self.tipo_ultimo_reporte == "ventas_mes":
                # Pasar información adicional del mes/año si está disponible
                mes = self.ultimo_reporte.get('mes', None)
                año = self.ultimo_reporte.get('año', None)
                if mes and año:
                    nombres_meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                    mes_nombre = nombres_meses[mes]
                    pdf_gen.generar_ventas_mes_personalizado(
                        self.ultimo_reporte['resultados'], 
                        self.ultimo_reporte['totales'],
                        f"{mes_nombre} {año}"
                    )
                else:
                    pdf_gen.generar_ventas_mes(
                        self.ultimo_reporte['resultados'], 
                        self.ultimo_reporte['totales']
                    )
            
            pdf_gen.guardar()
            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a:\n{archivo}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")