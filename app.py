import pyRofex
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configurar la conexión con pyRofex
pyRofex.initialize(
    user="jporta",
    password="JP$pm2024",
    account="58035",
    environment=pyRofex.Environment.LIVE
)

# Función para obtener datos históricos
def get_historical_data(ticker, start_date, end_date):
    data = []
    current_date = start_date
    while current_date <= end_date:
        response = pyRofex.get_market_data(
            ticker=ticker,
            entries=[pyRofex.MarketDataEntry.TRADE],
            date_from=current_date.strftime('%Y-%m-%d'),
            date_to=(current_date + timedelta(days=1)).strftime('%Y-%m-%d')
        )
        if 'marketData' in response and 'TRADES' in response['marketData']:
            trades = response['marketData']['TRADES']
            for trade in trades:
                data.append({
                    'date': trade['timestamp'],
                    'price': trade['price'],
                    'size': trade['size']
                })
        current_date += timedelta(days=1)
    return pd.DataFrame(data)

# Obtener datos históricos del bono AL30
ticker = "MERV - XMEV - AL30 - CI"
start_date = datetime(2023, 1, 1)  # Fecha de inicio (ajustar según sea necesario)
end_date = datetime(2023, 12, 31)  # Fecha de fin (ajustar según sea necesario)
data = get_historical_data(ticker, start_date, end_date)

# Convertir la columna 'date' a formato datetime
data['date'] = pd.to_datetime(data['date'])

# Título de la aplicación
st.title("Gráfico Histórico del Bono AL30")

# Mostrar los datos en la aplicación
st.subheader('Datos Históricos del AL30')
st.write(data)

# Crear un gráfico
st.subheader('Gráfico del Precio Histórico del AL30')

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
