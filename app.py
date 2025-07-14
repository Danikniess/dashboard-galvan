# app.py - Galvan Real Estate Intelligence Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Galvan Intelligence Dashboard")

# --- Carregamento dos Dados ---
# Idealmente, isso viria de um Google Sheets ou banco de dados.
# Por enquanto, usamos os dados do nosso exemplo.
@st.cache_data # Cache para performance
def load_data():
    data = {
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
        'Ano': [2024]*7 + [2025]*7,
        'N° de Imóveis Lançados': [110, 95, 125, 130, 140, 120, 115] + [135, 115, 150, 160, 175, 155, 140],
        'N° de Unidades Vendidas': [90, 85, 115, 120, 130, 105, 100] + [110, 105, 140, 155, 170, 145, 130],
        'VGV (R$ Milhões)': [45, 43, 58, 62, 71, 55, 53] + [60.5, 58.8, 81.2, 93.0, 110.5, 89.9, 80.6],
        'Preço m² Joinville': [6800, 6950, 7050, 7150, 7250, 7300, 7400] + [7900, 8050, 8200, 8350, 8500, 8600, 8750],
        'Preço m² Saguaçu': [8200, 8350, 8500, 8600, 8750, 8850, 8950] + [9800, 9950, 10150, 10300, 10500, 10650, 10800],
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# --- Barra Lateral com Filtros ---
st.sidebar.image("https://galvan.com.br/wp-content/themes/galvan-theme/assets/images/logo.png", width=150) # Exemplo de logo
st.sidebar.title("Filtros")
selected_year = st.sidebar.selectbox("Selecione o Ano de Análise", [2025, 2024])

# --- Corpo Principal do Dashboard ---
st.title("📈 Galvan Intelligence Dashboard")
st.markdown(f"Análise de performance do mercado imobiliário de Joinville - **Ano: {selected_year}**")

# Filtrando os dados pelo ano selecionado
df_2024 = df[df['Ano'] == 2024].reset_index()
df_2025 = df[df['Ano'] == 2025].reset_index()
df_selected = df[df['Ano'] == selected_year]

# --- KPIs em Destaque ---
col1, col2, col3 = st.columns(3)
unidades_vendidas_ultimo_mes = df_selected['N° de Unidades Vendidas'].iloc[-1]
vgv_ultimo_mes = df_selected['VGV (R$ Milhões)'].iloc[-1]
preco_saguacu_ultimo_mes = df_selected['Preço m² Saguaçu'].iloc[-1]

col1.metric("Unidades Vendidas (Último Mês)", f"{unidades_vendidas_ultimo_mes}")
col2.metric("VGV (Último Mês)", f"R$ {vgv_ultimo_mes} Milhões")
col3.metric("Preço m² Saguaçu (Último Mês)", f"R$ {preco_saguacu_ultimo_mes:,.2f}")

st.markdown("---")

# --- Gráficos Interativos ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Comparativo de Unidades Vendidas")
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(df_2025['Mês']))
    width = 0.35
    ax.bar(x - width/2, df_2024['N° de Unidades Vendidas'], width, label='2024', color='skyblue')
    ax.bar(x + width/2, df_2025['N° de Unidades Vendidas'], width, label='2025', color='blue')
    ax.set_ylabel('Número de Unidades')
    ax.set_title('Unidades Vendidas por Mês (2024 vs. 2025)')
    ax.set_xticks(x)
    ax.set_xticklabels(df_2025['Mês'])
    ax.legend()
    st.pyplot(fig)

with col_graf2:
    st.subheader("Variação do Preço por m²")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_2025['Mês'], df_2025['Preço m² Joinville'], marker='o', linestyle='-', color='blue', label='Joinville 2025')
    ax.plot(df_2025['Mês'], df_2025['Preço m² Saguaçu'], marker='s', linestyle='-', color='green', label='Saguaçu 2025')
    ax.plot(df_2024['Mês'], df_2024['Preço m² Joinville'], marker='o', linestyle='--', color='lightblue', label='Joinville 2024')
    ax.plot(df_2024['Mês'], df_2024['Preço m² Saguaçu'], marker='s', linestyle='--', color='lightgreen', label='Saguaçu 2024')
    ax.set_ylabel('Preço (R$)')
    ax.set_title('Preço Médio por m² (2024 vs. 2025)')
    ax.legend()
    st.pyplot(fig)


st.markdown("---")
# --- Tabela de Dados ---
st.subheader(f"Dados Consolidados de {selected_year}")
st.dataframe(df_selected)

@st.cache_data
def convert_df_to_csv(df_to_convert):
    return df_to_convert.to_csv().encode('utf-8')

csv = convert_df_to_csv(df_selected)

st.download_button(
    label="📥 Baixar dados como CSV",
    data=csv,
    file_name=f'dados_mercado_{selected_year}.csv',
    mime='text/csv',
)
