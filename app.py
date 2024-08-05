import pyRofex
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

# Configurar la conexión con pyRofex
pyRofex.initialize(
    user="jporta",
    password="JP$pm2024",
    account="58035",
    environment=pyRofex.Environment.LIVE
)

# Función para obtener datos actuales del mercado
def get_market_data(ticker):
    response = pyRofex.get_market_data(
        ticker=ticker,
        entries=[pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]
    )
    return response

# Ticker del bono AL30
ticker = "MERV - XMEV - AL30 - CI"

# Obtener datos actuales del mercado
market_data = get_market_data(ticker)

# Procesar la respuesta de la API
if 'marketData' in market_data and 'LA' in market_data['marketData']:
    last_trade = market_data['marketData']['LA']
    data = pd.DataFrame([{
        'date': datetime.now(),
        'price': last_trade['price'],
        'size': last_trade['size']
    }])
else:
    st.error("No se pudieron obtener los datos de mercado del bono AL30.")
    data = pd.DataFrame(columns=['date', 'price', 'size'])

# Convertir la columna 'date' a formato datetime
data['date'] = pd.to_datetime(data['date'])

# Título de la aplicación
st.title("Gráfico de Datos de Mercado del Bono AL30")

# Mostrar los datos en la aplicación
st.subheader('Datos de Mercado del AL30')
st.write(data)

# Crear un gráfico
st.subheader('Gráfico del Precio Actual del AL30')

fig, ax = plt.subplots()
ax.plot(data['date'], data['price'], label='Precio AL30')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio')
ax.set_title('Evolución del Precio del AL30')
ax.legend()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Opcional: agregar controles de filtrado en la aplicación
st.sidebar.header("Opciones de Filtrado")
start_date_filter = st.sidebar.date_input("Fecha de inicio", data['date'].min())
end_date_filter = st.sidebar.date_input("Fecha de fin", data['date'].max())

# Filtrar los datos según las fechas seleccionadas
filtered_data = data[(data['date'] >= pd.to_datetime(start_date_filter)) & (data['date'] <= pd.to_datetime(end_date_filter))]

# Mostrar los datos filtrados en la aplicación
st.subheader('Datos Filtrados')
st.write(filtered_data)

# Crear un gráfico con los datos filtrados
fig_filtered, ax_filtered = plt.subplots()
ax_filtered.plot(filtered_data['date'], filtered_data['price'], label='Precio AL30')
ax_filtered.set_xlabel('Fecha')
ax_filtered.set_ylabel('Precio')
ax_filtered.set_title('Evolución del Precio del AL30 (Filtrado)')
ax_filtered.legend()

# Mostrar el gráfico filtrado en Streamlit
st.pyplot(fig_filtered)

