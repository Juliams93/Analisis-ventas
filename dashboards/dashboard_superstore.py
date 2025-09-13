import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import sys
import os

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('data/superstore.csv', encoding='utf-8')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

st.title('Dashboard de Ventas - Superstore')

# KPIs
st.subheader('KPIs Clave')
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
ticket_avg = total_sales / total_orders
col1, col2, col3, col4 = st.columns(4)
col1.metric('Ventas Totales', f"${total_sales:,.0f}")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dashboards')))
# Filtros
def load_data():
    df = pd.read_csv('../data/superstore.csv', encoding='utf-8')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df
st.sidebar.header('Filtros')
segment = st.sidebar.multiselect('Segmento', df['Segment'].unique(), default=list(df['Segment'].unique()))
region = st.sidebar.multiselect('Región', df['Region'].unique(), default=list(df['Region'].unique()))
df_filtered = df[df['Segment'].isin(segment) & df['Region'].isin(region)]

# Tendencia de ventas
st.subheader('Tendencia de Ventas en el Tiempo')
df_time = df_filtered.groupby(pd.Grouper(key='Order Date', freq='M')).agg({'Sales':'sum'}).reset_index()
fig = px.line(df_time, x='Order Date', y='Sales', title='Ventas Mensuales')
st.plotly_chart(fig, use_container_width=True)

# Predicción de demanda (ventas)
st.subheader('Predicción de Ventas (Modelo Simple)')
df_time['Month'] = np.arange(len(df_time))
X = df_time[['Month']]
y = df_time['Sales']
model = LinearRegression()
model.fit(X, y)
future_months = 6
future_X = np.arange(len(df_time), len(df_time)+future_months).reshape(-1,1)
pred_sales = model.predict(future_X)

future_dates = pd.date_range(df_time['Order Date'].max() + pd.offsets.MonthBegin(), periods=future_months, freq='M')
df_pred = pd.DataFrame({'Order Date': future_dates, 'Sales': pred_sales})
fig_pred = px.line(pd.concat([df_time[['Order Date','Sales']], df_pred]), x='Order Date', y='Sales', title='Ventas Reales y Predichas')
st.plotly_chart(fig_pred, use_container_width=True)

st.caption('Dashboard interactivo de ventas y predicción de demanda para empresas.')

# Conclusiones del análisis
st.header('Conclusiones del análisis')
st.markdown(f'''
- Las ventas totales analizadas fueron de ${total_sales:,.0f}, con una ganancia total de $ {total_profit:,.0f} y un ticket promedio de ${ticket_avg:,.2f}.
- El número de órdenes únicas fue de {total_orders}, mostrando un flujo constante de transacciones.
- La tendencia de ventas muestra variaciones mensuales, lo que sugiere estacionalidad o impacto de campañas.
- La predicción de demanda indica que las ventas seguirán una tendencia similar en los próximos meses, útil para planificación.
- El uso de filtros permite identificar segmentos y regiones con mejor desempeño, facilitando la toma de decisiones focalizadas.
''')

