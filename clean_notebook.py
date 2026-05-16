import nbformat
import re
import os

def clean_notebook(input_file, output_file):
    """
    Limpia un notebook Jupyter removiendo imágenes embebidas en base64
    
    Args:
        input_file: Ruta del archivo .ipynb original
        output_file: Ruta del archivo .ipynb limpio
    """
    
    try:
        # Cargar el notebook
        print(f"📂 Cargando notebook: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        print(f"✅ Notebook cargado correctamente")
        
        # Contador de imágenes removidas
        images_removed = 0
        
        # Procesar cada celda
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                original_source = cell.source
                
                # Patrón para detectar imágenes base64
                # Elimina: ![nombre](data:image/png;base64,...)
                pattern = r'!\[([^\]]*)\]\(data:image/[^;]+;base64,[^)]+\)'
                
                # Reemplazar con referencia simple
                new_source = re.sub(pattern, r'![Imagen removida: \1]', original_source)
                
                # Contar imágenes removidas
                if new_source != original_source:
                    images_removed += re.findall(pattern, original_source).__len__()
                    cell.source = new_source
        
        # Guardar el notebook limpio
        print(f"💾 Guardando notebook limpio: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        # Comparar tamaños
        original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
        clean_size = os.path.getsize(output_file) / (1024 * 1024)    # MB
        reduction = ((original_size - clean_size) / original_size) * 100
        
        print(f"\n📊 Resumen:")
        print(f"   • Imágenes base64 removidas: {images_removed}")
        print(f"   • Tamaño original: {original_size:.2f} MB")
        print(f"   • Tamaño limpio: {clean_size:.2f} MB")
        print(f"   • Reducción: {reduction:.1f}%")
        print(f"\n✨ ¡Notebook limpiado exitosamente!")
        
    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado: {input_file}")
    except Exception as e:
        print(f"❌ Error al procesar el notebook: {str(e)}")

# Ejecutar la limpieza
if __name__ == "__main__":
    input_notebook = 'Caso_Practico_Forecast.ipynb'
    output_notebook = 'Caso_Practico_Forecast_LIMPIO.ipynb'
    
    clean_notebook(input_notebook, output_notebook)
