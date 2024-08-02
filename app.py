pip install -r requisitos.txt

import pyRofex
import time
import pandas as pd
import streamlit as st

# Configurar la conexión con pyRofex
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

# Inicializar Streamlit
st.title("Market Data Stream")
data_placeholder = st.empty()

def market_data_handler(message):
    datos = {
        "ticker": message["instrumentId"]["symbol"],
        "bids": message["marketData"]["BI"],
        "offer": message["marketData"]["OF"]
    }
    df_bids = pd.DataFrame(datos['bids'], columns=['price', 'size']).set_index("price")
    df_offers = pd.DataFrame(datos['offer'], columns=['price', 'size']).set_index("price")
    
    ticker = datos['ticker']
    
    data_placeholder.subheader(f"Market Data for {ticker}")
    data_placeholder.write("Bids:")
    data_placeholder.dataframe(df_bids)
    data_placeholder.write("Offers:")
    data_placeholder.dataframe(df_offers)

def error_handler(message):
    st.error(f"Error: {message}")

def exception_handler(e):
    st.error(f"Exception Occurred: {e.msg}")

# Inicializar conexión WebSocket con los handlers
pyRofex.init_websocket_connection(
    market_data_handler=market_data_handler,
    error_handler=error_handler,
    exception_handler=exception_handler,
)

# Suscribirse para recibir mensajes de datos del mercado
instruments = [
    "MERV - XMEV - AL30 - CI",
    "MERV - XMEV - AL30D - CI",
    "MERV - XMEV - AL30C - CI",
    "MERV - XMEV - GD30 - CI",
    "MERV - XMEV - GD30C - CI",
    "MERV - XMEV - GD30D - CI"
]
entries = [
    pyRofex.MarketDataEntry.BIDS,
    pyRofex.MarketDataEntry.OFFERS,
]

pyRofex.market_data_subscription(tickers=instruments, entries=entries, depth=5)
