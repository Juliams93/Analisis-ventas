import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

st.title('EDA Interactivo - Superstore')

file_path = './data/superstore.csv'
if not os.path.exists(file_path):
    st.write(f"Directorio actual: {os.getcwd()}")
    st.error(f'No se encontró el archivo {file_path}.')
    st.stop()

df = pd.read_csv(file_path, encoding='utf-8')

# Limpieza de datos
st.header('Limpieza de datos')
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_')
if 'Order_Date' in df.columns:
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
if 'Ship_Date' in df.columns:
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
if 'Postal_Code' in df.columns:
    df['Postal_Code'] = df['Postal_Code'].astype(str)
df = df.drop_duplicates()
df = df.dropna()

# Resumen general
st.header('Resumen general')
st.write('Dimensiones:', df.shape)
st.write('Tipos de datos:')
st.write(df.dtypes)
st.write('Primeras filas:')
st.dataframe(df.head())
st.write('Descripción estadística:')
st.write(df.describe())
st.write('Valores nulos por columna:')
st.write(df.isnull().sum())

# Outliers en ventas y ganancias
st.header('Outliers')
fig1, ax1 = plt.subplots()
sns.boxplot(x=df['Sales'], ax=ax1)
st.pyplot(fig1)
if 'Profit' in df.columns:
    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df['Profit'], ax=ax2)
    st.pyplot(fig2)

# Distribución de ventas
st.header('Distribución de Ventas')
fig3, ax3 = plt.subplots()
sns.histplot(df['Sales'], bins=50, kde=True, ax=ax3)
st.pyplot(fig3)

# Correlación
if 'Profit' in df.columns:
    st.header('Correlación Ventas-Ganancia')
    fig4, ax4 = plt.subplots()
    sns.heatmap(df[['Sales','Profit']].corr(), annot=True, cmap='coolwarm', ax=ax4)
    st.pyplot(fig4)

# Ventas por categoría
if 'Category' in df.columns:
    st.header('Ventas por Categoría')
    fig5, ax5 = plt.subplots()
    sns.barplot(x='Category', y='Sales', data=df, estimator=sum, ax=ax5)
    st.pyplot(fig5)

# Top 10 subcategorías
if 'Sub_Category' in df.columns:
    st.header('Top 10 Subcategorías por Ventas')
    fig6, ax6 = plt.subplots()
    top_sub = df.groupby('Sub_Category')['Sales'].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=top_sub.index, y=top_sub.values, ax=ax6)
    plt.xticks(rotation=45)
    st.pyplot(fig6)

# Top 10 clientes
if 'Customer_Name' in df.columns:
    st.header('Top 10 Clientes por Ventas')
    fig7, ax7 = plt.subplots()
    top_customers = df.groupby('Customer_Name')[['Sales','Profit']].sum().sort_values('Sales', ascending=False).head(10)
    sns.barplot(x=top_customers.index, y=top_customers['Sales'], ax=ax7)
    plt.xticks(rotation=45)
    st.pyplot(fig7)

# Análisis temporal
if 'Order_Date' in df.columns:
    st.header('Ventas por Mes')
    df['Month'] = df['Order_Date'].dt.month
    fig8, ax8 = plt.subplots()
    sns.lineplot(x='Month', y='Sales', data=df.groupby('Month')['Sales'].sum().reset_index(), ax=ax8)
    st.pyplot(fig8)

    st.header('Ventas por Día de la Semana')
    df['DayOfWeek'] = df['Order_Date'].dt.day_name()
    fig9, ax9 = plt.subplots()
    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    sns.barplot(x='DayOfWeek', y='Sales', data=df.groupby('DayOfWeek')['Sales'].sum().reindex(order).reset_index(), ax=ax9)
    st.pyplot(fig9)

# Mapa de calor ventas por región y segmento
if 'Region' in df.columns and 'Segment' in df.columns:
    st.header('Mapa de calor: Ventas por Región y Segmento')
    pivot = df.pivot_table(index='Region', columns='Segment', values='Sales', aggfunc='sum')
    fig10, ax10 = plt.subplots()
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu', ax=ax10)
    st.pyplot(fig10)

# Valores únicos
st.header('Valores únicos por columna')
st.write(df.nunique())

# Conclusiones del análisis
st.header('Conclusiones del análisis')
st.markdown('''
- Las ventas presentan outliers, lo que indica operaciones excepcionales o posibles errores de captura.
- Existe correlación positiva entre ventas y ganancia, aunque no perfecta.
- Las categorías y subcategorías muestran que ciertos productos concentran la mayor parte de las ventas.
- Un pequeño grupo de clientes representa un alto porcentaje de las ventas totales (clientes top).
- Se observa estacionalidad en las ventas por mes y diferencias claras entre días de la semana.
- Algunas regiones y segmentos son mucho más rentables que otros, lo que puede guiar estrategias comerciales.
''')

st.write('EDA completado.')

