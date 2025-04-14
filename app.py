import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(page_title="Análisis Completo - Alianza Lima", layout="wide")
st.title("📊 Análisis Completo - Alianza Lima")

# =============================
# 📂 Carga de datos
# =============================
try:
    df_maestro = pd.read_csv('df_maestro.csv')
except FileNotFoundError:
    st.error("❌ No se encontró 'df_maestro.csv'. Por favor, expórtalo desde Jupyter:\n\n df_maestro.to_csv('df_maestro.csv', index=False)")
    st.stop()

# =============================
# 🎛️ Sidebar - Selección de Partido
# =============================
partido_elegido = st.sidebar.selectbox(
    'Selecciona el partido que quieres analizar:',
    df_maestro['Partido'].unique()
)

# =============================
# Funciones de radar
# =============================

def generar_radar(partido, categorias, color, titulo):
    index = df_maestro[df_maestro['Partido'] == partido].index[0]
    valores = df_maestro.loc[index, categorias].values
    max_valores = np.max(df_maestro[categorias].values, axis=0)
    valores_normalizados = [val / max_val if max_val != 0 else 0 for val, max_val in zip(valores, max_valores)]
    valores_normalizados += [valores_normalizados[0]]

    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores_normalizados, color=color, linewidth=2)
    ax.fill(angulos, valores_normalizados, color=color, alpha=0.25)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias, fontsize=10)
    plt.title(f"{titulo}: {partido}", size=13, y=1.1)
    st.pyplot(fig)

# =============================
# 📊 Gráficos resumen por partido
# =============================

def grafico_resumen(partido, columna, color, titulo, ylabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    partidos = df_maestro['Partido']
    valores = df_maestro[columna]
    ax.plot(partidos, valores, marker='o', color=color)
    ax.axvline(x=partido, color='gray', linestyle='--', alpha=0.7)
    ax.set_title(titulo)
    ax.set_xlabel('Partido')
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# =============================
# 📋 Resumen General del Partido
# =============================
st.header(f"📋 Resumen del partido: {partido_elegido}")
df_partido = df_maestro[df_maestro['Partido'] == partido_elegido]
st.dataframe(df_partido.T)

# =============================
# 📊 Gráficos Resumen Globales
# =============================
st.subheader("📈 Gráficos Resumen del Equipo")

grafico_resumen(partido_elegido, 'xG', 'blue', 'Evolución de xG por Partido', 'xG')
grafico_resumen(partido_elegido, 'Goles recibidos', 'red', 'Goles Recibidos por Partido', 'Goles Recibidos')
grafico_resumen(partido_elegido, 'PPDA', 'green', 'Presión Defensiva (PPDA)', 'PPDA')
grafico_resumen(partido_elegido, 'Intensidad de paso', 'orange', 'Intensidad de Pase', 'Intensidad')

# =============================
# 🧭 Radar Global Resumen
# =============================
st.subheader("🌟 Radar Global Resumen")
generar_radar(partido_elegido, ['xG', 'Goles recibidos', 'Pases progresivos', 'Intensidad de paso'], 'magenta', 'Radar Global Resumen')

# =============================
# 🧩 Radares por Área
# =============================

# Definimos las categorías por radar
categorias_ofensiva = ['xG', 'Tiros', 'Centros precisos']
categorias_defensiva = ['Goles recibidos', 'Tiros en contra', 'Interceptaciones']
categorias_organizacion = ['Pases progresivos', 'Desmarques']
categorias_indices = ['Intensidad de paso', 'PPDA']

st.subheader("⚽ Radar Ofensivo")
generar_radar(partido_elegido, categorias_ofensiva, 'blue', 'Radar Ofensivo')

st.subheader("🛡️ Radar Defensivo")
generar_radar(partido_elegido, categorias_defensiva, 'red', 'Radar Defensivo')

st.subheader("🧩 Radar Organizacional")
generar_radar(partido_elegido, categorias_organizacion, 'orange', 'Radar Organizacional')

st.subheader("📊 Radar Índices Generales")
generar_radar(partido_elegido, categorias_indices, 'green', 'Radar Índices Generales')

# =============================
# ✅ Fin de la app
# =============================
st.success("✅ Análisis completo generado correctamente.")
st.markdown("💡 Puedes seguir seleccionando diferentes partidos desde el menú lateral para visualizar su análisis.")
