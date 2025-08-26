import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

CSV_FILE = 'dados_rede.csv'

st.set_page_config(page_title="Dashboard de Métricas da Rede", layout="wide")
st.title("📡 Dashboard Avançado de Métricas da Rede")

# Atualiza automaticamente a cada 5 segundos
st_autorefresh(interval=5000, key="auto_refresh")

# Limites de alerta
RSSI_FRACO = -70
LATENCIA_ALTA = 100  # ms
PERDA_ALTA = 10      # %

try:
    # Define os nomes das colunas caso o CSV não tenha cabeçalho
    colunas = ['timestamp','SSID','BSSID','canal','IP_local','RSSI','latencia_ms','perda_pct',
               'pacotes_enviados','pacotes_recebidos','taxa_sucesso_pct']
    
    df = pd.read_csv(CSV_FILE, names=colunas, header=None, parse_dates=['timestamp'], dayfirst=False)
    
    if df.empty:
        st.write("Nenhuma métrica disponível ainda.")
    else:
        # Selectbox de rede (fixo, key única)
        ssids = df['SSID'].unique()
        ssid_selecionado = st.selectbox("Escolha a rede", ssids, key="rede_selectbox")
        df_filtrado = df[df['SSID'] == ssid_selecionado].copy()
        
        st.subheader("Últimas métricas")

        # Cards de indicadores
        col1, col2, col3 = st.columns(3)
        col1.metric("RSSI Médio (dBm)", f"{df_filtrado['RSSI'].mean():.1f}",
                    delta=None,
                    delta_color="inverse" if df_filtrado['RSSI'].mean() < RSSI_FRACO else "normal")
        col2.metric("Latência Média (ms)", f"{df_filtrado['latencia_ms'].mean():.1f}",
                    delta=None,
                    delta_color="inverse" if df_filtrado['latencia_ms'].mean() > LATENCIA_ALTA else "normal")
        col3.metric("Perda Média (%)", f"{df_filtrado['perda_pct'].mean():.1f}",
                    delta=None,
                    delta_color="inverse" if df_filtrado['perda_pct'].mean() > PERDA_ALTA else "normal")

        # Dataframe com últimas 10 métricas
        st.dataframe(df_filtrado.tail(10))

        # Gráfico de séries temporais
        st.subheader("Gráficos com alertas")
        df_plot = df_filtrado.set_index('timestamp')[['RSSI','latencia_ms','perda_pct']]
        st.line_chart(df_plot)

        # Função de highlight das métricas
        def highlight(row):
            styles = []
            styles.append(f'background-color: {"red" if row.RSSI < RSSI_FRACO else "green"}')
            styles.append(f'background-color: {"red" if row.latencia_ms > LATENCIA_ALTA else "green"}')
            styles.append(f'background-color: {"red" if row.perda_pct > PERDA_ALTA else "green"}')
            styles += [''] * (len(row)-3)  # mantém os outros campos sem cor
            return styles

        st.dataframe(df_filtrado.tail(10).style.apply(highlight, axis=1))

except Exception as e:
    st.write("Erro ao carregar dados: " + str(e))
