import streamlit as st
import os
from PIL import Image

st.title('Visualización de Gráficas EDA - Superstore')

figures_dir = '../figures'

# Diccionario de descripciones automáticas
descripciones = {
    'outliers_ventas.png': 'Boxplot que muestra los valores atípicos (outliers) en las ventas. Permite identificar ventas inusualmente altas o bajas.',
    'outliers_ganancia.png': 'Boxplot de outliers en la ganancia. Ayuda a detectar operaciones con márgenes inusuales.',
    'distribucion_ventas.png': 'Histograma de la distribución de ventas. Muestra la frecuencia de distintos rangos de ventas.',
    'correlacion_ventas_ganancia.png': 'Mapa de calor de correlación entre ventas y ganancia. Un valor alto indica que a mayor venta, mayor ganancia.',
    'ventas_categoria.png': 'Ventas totales agrupadas por categoría de producto. Permite ver qué línea de productos es más fuerte.',
    'top10_subcategorias.png': 'Top 10 subcategorías por ventas. Identifica los productos estrella.',
    'top10_clientes.png': 'Top 10 clientes por ventas. Útil para estrategias de fidelización.',
    'ventas_mes.png': 'Ventas totales por mes. Permite analizar estacionalidad y tendencias mensuales.',
    'ventas_dia_semana.png': 'Ventas por día de la semana. Ayuda a identificar los días con mayor actividad.',
    'mapa_calor_region_segmento.png': 'Mapa de calor de ventas por región y segmento. Visualiza zonas y segmentos más rentables.'
}

if not os.path.exists(figures_dir):
    st.error('La carpeta figures no existe. Ejecuta primero el script de EDA.')
else:
    images = [f for f in os.listdir(figures_dir) if f.endswith('.png')]
    if not images:
        st.warning('No se encontraron imágenes en la carpeta figures.')
    else:
        for img_name in sorted(images):
            titulo = img_name.replace('_',' ').replace('.png','').capitalize()
            st.subheader(titulo)
            img_path = os.path.join(figures_dir, img_name)
            image = Image.open(img_path)
            desc = descripciones.get(img_name, 'Gráfica generada por el EDA.')
            st.image(image, caption=desc, use_column_width=True)
