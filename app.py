import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Gráfico Histórico del Bono AL30")

# Cargar los datos históricos desde un archivo CSV
@st.cache
def load_data():
    data = pd.read_csv('AL30_historico.csv', parse_dates=['date'])
    return data

data = load_data()

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
start_date = st.sidebar.date_input("Fecha de inicio", data['date'].min())
end_date = st.sidebar.date_input("Fecha de fin", data['date'].max())

# Filtrar los datos según las fechas seleccionadas
filtered_data = data[(data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))]

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
