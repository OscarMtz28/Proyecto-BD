"""
Utilidades para ordenamiento de tablas
"""

class TableSorter:
    """Clase para manejar el ordenamiento de tablas Treeview"""
    
    @staticmethod
    def sort_treeview(tree, col, sort_column_var, sort_reverse_var, numeric_columns=None):
        """
        Ordenar un Treeview por columna
        
        Args:
            tree: El widget Treeview
            col: Columna a ordenar
            sort_column_var: Variable que almacena la columna actual de ordenamiento
            sort_reverse_var: Variable que almacena la dirección de ordenamiento
            numeric_columns: Lista de columnas que deben ordenarse numéricamente
        """
        numeric_columns = numeric_columns or []
        
        # Determinar si cambiar dirección de ordenamiento
        if sort_column_var == col:
            sort_reverse_var = not sort_reverse_var
        else:
            sort_column_var = col
            sort_reverse_var = False
        
        # Obtener todos los elementos
        items = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        # Ordenar según el tipo de columna
        if col in numeric_columns:
            # Ordenamiento numérico
            if col == 'Total':
                # Para columnas con formato de moneda
                items.sort(key=lambda x: float(x[0].replace('$', '')) if x[0] and '$' in str(x[0]) else 0, 
                          reverse=sort_reverse_var)
            else:
                # Para columnas numéricas normales
                items.sort(key=lambda x: float(x[0]) if x[0] and str(x[0]).replace('.', '').replace('-', '').isdigit() else 0, 
                          reverse=sort_reverse_var)
        else:
            # Ordenamiento alfabético
            items.sort(key=lambda x: str(x[0]).lower(), reverse=sort_reverse_var)
        
        # Reorganizar elementos en el treeview
        for index, (val, child) in enumerate(items):
            tree.move(child, '', index)
        
        return sort_column_var, sort_reverse_var
    
    @staticmethod
    def update_header_indicators(tree, col, sort_reverse, columns):
        """
        Actualizar indicadores visuales en las cabeceras
        
        Args:
            tree: El widget Treeview
            col: Columna actualmente ordenada
            sort_reverse: Dirección del ordenamiento
            columns: Lista de todas las columnas
        """
        for column in columns:
            if column == col:
                # Agregar flecha indicadora
                arrow = " ↓" if sort_reverse else " ↑"
                tree.heading(column, text=column + arrow)
            else:
                # Remover flecha de otras columnas
                tree.heading(column, text=column)