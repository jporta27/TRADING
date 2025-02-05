import pyRofex
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Configurar los parámetros del entorno
pyRofex._set_environment_parameter(
    "url", "https://api.lbo.xoms.com.ar/", pyRofex.Environment.LIVE
)
pyRofex._set_environment_parameter(
    "ws", "wss://api.lbo.xoms.com.ar/", pyRofex.Environment.LIVE
)
pyRofex._set_environment_parameter("proprietary", "API", pyRofex.Environment.LIVE)

# Inicializar el entorno
pyRofex.initialize(
    user="jporta",
    password="JP$pm2024",
    account="58035",
    environment=pyRofex.Environment.LIVE
)

# Variables globales para almacenar datos intradiarios
intraday_data = []

# Configurar la aplicación de Streamlit
st.title("Datos Intradiarios del Bono AL30")
placeholder = st.empty()

# Función para manejar los datos de mercado recibidos
def market_data_handler(message):
    global intraday_data
    if 'marketData' in message and 'LA' in message['marketData']:
        last_trade = message['marketData']['LA']
        if last_trade:
            trade_data = {
                'date': datetime.now(),
                'price': last_trade['price'],
                'size': last_trade['size']
            }
            intraday_data.append(trade_data)
            update_display()

# Función para actualizar la visualización en Streamlit
def update_display():
    data_df = pd.DataFrame(intraday_data)
    if not data_df.empty:
        # Convertir la columna 'date' a formato datetime
        data_df['date'] = pd.to_datetime(data_df['date'])

        # Crear un gráfico
        fig, ax = plt.subplots()
        ax.plot(data_df['date'], data_df['price'], label='Precio AL30')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Precio')
        ax.set_title('Evolución del Precio Intradiario del AL30')
        ax.legend()

        # Mostrar el gráfico en Streamlit
        placeholder.pyplot(fig)

# Función para manejar errores
def error_handler(message):
    st.error(f"Error recibido: {message}")

# Función para manejar excepciones
def exception_handler(e):
    st.error(f"Excepción recibida: {e}")

# Inicializar la conexión WebSocket con los handlers
pyRofex.init_websocket_connection(
    market_data_handler=market_data_handler,
    error_handler=error_handler,
    exception_handler=exception_handler,
)

# Ticker del bono AL30
ticker = "MERV - XMEV - AL30 - CI"

# Suscribirse a los datos de mercado en tiempo real
pyRofex.market_data_subscription(
    tickers=[ticker],
    entries=[pyRofex.MarketDataEntry.LAST]
)

# Mantener la aplicación en ejecución para recibir datos en tiempo real
st.write("Esperando datos en tiempo real del bono AL30...")
