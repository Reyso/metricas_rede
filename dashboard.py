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
        # Escolha automática da rede (pega a mais recente)
        ssid_mais_recente = df.iloc[-1]['SSID']
        df_filtrado = df[df['SSID'] == ssid_mais_recente].copy()
        
        st.subheader(f"Últimas métricas da rede: **{ssid_mais_recente}**")

        # Cards de indicadores
        col1, col2, col3 = st.columns(3)
        col1.metric("RSSI Médio (dBm)", f"{df_filtrado['RSSI'].mean():.1f}")
        col2.metric("Latência Média (ms)", f"{df_filtrado['latencia_ms'].mean():.1f}")
        col3.metric("Perda Média (%)", f"{df_filtrado['perda_pct'].mean():.1f}")

        # Função de highlight das métricas
        def highlight(row):
            styles = [''] * len(row)
            if row['RSSI'] < RSSI_FRACO:
                styles[df_filtrado.columns.get_loc('RSSI')] = 'background-color: red'
            if row['latencia_ms'] > LATENCIA_ALTA:
                styles[df_filtrado.columns.get_loc('latencia_ms')] = 'background-color: red'
            if row['perda_pct'] > PERDA_ALTA:
                styles[df_filtrado.columns.get_loc('perda_pct')] = 'background-color: red'
            return styles

        st.subheader("Últimas 10 medições")
        st.dataframe(df_filtrado.tail(10).style.apply(highlight, axis=1))

        # Gráficos separados em grade 2x2
        st.subheader("📊 Métricas individuais")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("RSSI (dBm) - Quanto mais próximo de 0, melhor o sinal.")
            st.line_chart(df_filtrado.set_index('timestamp')['RSSI'], use_container_width=True,color = '#ffaa00')
            
        with col2:
            st.subheader("Latência (ms) - Valores menores indicam melhor resposta da rede.")
            st.line_chart(df_filtrado.set_index('timestamp')['latencia_ms'], use_container_width=True, color = '#7707a3')
            

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Perda de Pacotes (%) - Ideal é ficar em 0%.")
            st.line_chart(df_filtrado.set_index('timestamp')['perda_pct'], use_container_width=True, color = '#f22718')
            
        with col4:
            st.subheader("Taxa de Sucesso (%) - Mostra confiabilidade da transmissão.")
            st.line_chart(df_filtrado.set_index('timestamp')['taxa_sucesso_pct'], use_container_width=True, color = '#16a81d')
            

except Exception as e:
    st.write("Erro ao carregar dados: " + str(e))
