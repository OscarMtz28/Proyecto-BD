"""
Generador de reportes en PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime

class PDFGenerator:
    """Clase para generar reportes en PDF"""
    
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Estilo personalizado para títulos
        self.titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.darkblue
        )
    
    def agregar_titulo(self, titulo):
        """Agregar título al reporte"""
        self.story.append(Paragraph(titulo, self.titulo_style))
        self.story.append(Spacer(1, 20))
    
    def agregar_fecha(self):
        """Agregar fecha de generación"""
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.story.append(Paragraph(f"Fecha de generación: {fecha_actual}", self.styles['Normal']))
        self.story.append(Spacer(1, 20))
    
    def agregar_parrafo(self, texto, estilo='Normal'):
        """Agregar párrafo de texto"""
        self.story.append(Paragraph(texto, self.styles[estilo]))
        self.story.append(Spacer(1, 10))
    
    def agregar_tabla(self, data, col_widths=None):
        """Agregar tabla al reporte"""
        if not col_widths:
            col_widths = [2*inch] * len(data[0])
        
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
    
    def generar_productos_vendidos(self, datos):
        """Generar reporte de productos más vendidos"""
        self.agregar_titulo("REPORTE DE PRODUCTOS MÁS VENDIDOS")
        self.agregar_fecha()
        
        if not datos:
            self.agregar_parrafo("No hay datos de productos vendidos disponibles.")
            return
        
        data = [['Producto', 'Cantidad Vendida', 'Ingresos Totales']]
        for producto, cantidad, ingresos in datos:
            # Manejar valores None de forma segura
            producto_str = str(producto) if producto is not None else "N/A"
            cantidad_str = str(cantidad) if cantidad is not None else "0"
            ingresos_num = float(ingresos) if ingresos is not None else 0.0
            data.append([producto_str, cantidad_str, f"${ingresos_num:.2f}"])
        
        self.agregar_tabla(data, [3*inch, 1.5*inch, 1.5*inch])
    
    def generar_ventas_cliente(self, datos):
        """Generar reporte de ventas por cliente"""
        self.agregar_titulo("REPORTE DE VENTAS POR CLIENTE")
        self.agregar_fecha()
        
        if not datos:
            self.agregar_parrafo("No hay datos de ventas por cliente disponibles.")
            return
        
        data = [['Cliente', 'Compras', 'Total Gastado', 'Puntos']]
        for cliente, compras, total, puntos in datos:
            # Manejar valores None de forma segura
            cliente_str = str(cliente) if cliente is not None else "N/A"
            compras_str = str(compras) if compras is not None else "0"
            total_num = float(total) if total is not None else 0.0
            puntos_str = str(puntos) if puntos is not None else "0"
            data.append([cliente_str, compras_str, f"${total_num:.2f}", puntos_str])
        
        self.agregar_tabla(data, [2.5*inch, 1*inch, 1.5*inch, 1*inch])
    
    def generar_stock_bajo(self, datos):
        """Generar reporte de stock bajo"""
        self.agregar_titulo("REPORTE DE PRODUCTOS CON STOCK BAJO")
        self.agregar_fecha()
        
        if not datos:
            self.agregar_parrafo("¡Excelente! Todos los productos tienen stock suficiente.")
            return
        
        data = [['Producto', 'Stock', 'Ubicación', 'Categoría']]
        for producto, stock, ubicacion, categoria in datos:
            # Manejar valores None de forma segura
            producto_str = str(producto) if producto is not None else "N/A"
            stock_str = str(stock) if stock is not None else "0"
            ubicacion_str = str(ubicacion) if ubicacion is not None else "N/A"
            categoria_str = str(categoria) if categoria is not None else "N/A"
            data.append([producto_str, stock_str, ubicacion_str, categoria_str])
        
        self.agregar_tabla(data, [2*inch, 1*inch, 1.5*inch, 1.5*inch])
    
    def generar_ventas_mes(self, datos_diarios, totales):
        """Generar reporte de ventas del mes"""
        mes_actual = datetime.now().strftime('%B %Y').upper()
        self.agregar_titulo(f"REPORTE DE VENTAS DEL MES - {mes_actual}")
        self.agregar_fecha()
        
        # Resumen del mes - manejar valores None
        self.agregar_parrafo("RESUMEN DEL MES:", 'Heading2')
        
        if totales and len(totales) >= 2:
            total_ventas = totales[0] if totales[0] is not None else 0
            ingresos_totales = totales[1] if totales[1] is not None else 0.0
        else:
            total_ventas = 0
            ingresos_totales = 0.0
        
        self.agregar_parrafo(f"Total de ventas: {total_ventas}")
        self.agregar_parrafo(f"Ingresos totales: ${ingresos_totales:.2f}")
        
        # Tabla de ventas diarias
        if datos_diarios and len(datos_diarios) > 0:
            data = [['Fecha', 'Ventas', 'Total del Día']]
            for fecha, ventas, total in datos_diarios:
                # Manejar valores None de forma segura
                fecha_str = str(fecha) if fecha is not None else "N/A"
                ventas_str = str(ventas) if ventas is not None else "0"
                total_num = float(total) if total is not None else 0.0
                data.append([fecha_str, ventas_str, f"${total_num:.2f}"])
            self.agregar_tabla(data, [2*inch, 1.5*inch, 1.5*inch])
        else:
            self.agregar_parrafo("No hay ventas registradas en este período.")
    
    def generar_ventas_mes_personalizado(self, datos_diarios, totales, periodo):
        """Generar reporte de ventas de un mes específico"""
        self.agregar_titulo(f"REPORTE DE VENTAS DEL MES - {periodo.upper()}")
        self.agregar_fecha()
        
        # Resumen del mes - manejar valores None de forma segura
        self.agregar_parrafo("RESUMEN DEL MES:", 'Heading2')
        
        if totales and len(totales) >= 2:
            total_ventas = totales[0] if totales[0] is not None else 0
            ingresos_totales = totales[1] if totales[1] is not None else 0.0
        else:
            total_ventas = 0
            ingresos_totales = 0.0
        
        self.agregar_parrafo(f"Total de ventas: {total_ventas}")
        self.agregar_parrafo(f"Ingresos totales: ${ingresos_totales:.2f}")
        
        # Tabla de ventas diarias
        if datos_diarios and len(datos_diarios) > 0:
            data = [['Fecha', 'Ventas', 'Total del Día']]
            for fecha, ventas, total in datos_diarios:
                # Manejar valores None de forma segura
                fecha_str = str(fecha) if fecha is not None else "N/A"
                ventas_str = str(ventas) if ventas is not None else "0"
                total_num = float(total) if total is not None else 0.0
                data.append([fecha_str, ventas_str, f"${total_num:.2f}"])
            self.agregar_tabla(data, [2*inch, 1.5*inch, 1.5*inch])
        else:
            self.agregar_parrafo(f"No hay ventas registradas en {periodo}.")
    
    def guardar(self):
        """Guardar el documento PDF"""
        self.doc.build(self.story)