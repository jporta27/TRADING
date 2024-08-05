import pyRofex
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

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
        entries=[pyRofex.MarketDataEntry.LAST]
    )
    return response

# Ticker del bono AL30
ticker = "MERV - XMEV - AL30 - CI"

# Obtener datos actuales del mercado
market_data = get_market_data(ticker)

# Procesar la respuesta de la API
data = []
if 'marketData' in market_data:
    if 'LA' in market_data['marketData']:
        last_trade = market_data['marketData']['LA']
        if last_trade:
            data.append({
                'date': datetime.now(),
                'price': last_trade['price'],
                'size': last_trade['size']
            })
    else:
        st.error("No se encontraron datos de la última transacción.")
else:
    st.error("Error al obtener los datos de mercado.")

# Crear un DataFrame
data_df = pd.DataFrame(data)

# Título de la aplicación
st.title("Gráfico de Datos de Mercado del Bono AL30")

if not data_df.empty:
    # Convertir la columna 'date' a formato datetime
    data_df['date'] = pd.to_datetime(data_df['date'])

    # Mostrar los datos en la aplicación
    st.subheader('Datos de Mercado del AL30')
    st.write(data_df)

    # Crear un gráfico
    st.subheader('Gráfico del Precio Actual del AL30')

    fig, ax = plt.subplots()
    ax.plot(data_df['date'], data_df['price'], label='Precio AL30')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio')
    ax.set_title('Evolución del Precio del AL30')
    ax.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
else:
    st.write("No hay datos disponibles para mostrar.")
