import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

CSV_FILE = 'dados_rede.csv'

# Atualiza automaticamente a cada 5 segundos
st_autorefresh(interval=5 * 1000, key="dashboard_autorefresh")

st.title("Dashboard de Métricas da Rede.")

try:
    # Define os nomes das colunas manualmente
    df = pd.read_csv(CSV_FILE, names=['timestamp','RSSI','latencia_ms','perda_pct'], header=None)
    st.write("Colunas detectadas:", df.columns.tolist())  # 🔹 debug

    # Converte timestamp para datetime e define como índice
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df.set_index('timestamp')

    # Seleciona colunas para plot
    plot_cols = ['RSSI', 'latencia_ms', 'perda_pct']

    st.subheader("Últimas métricas")
    st.dataframe(df[plot_cols].tail(10))

    st.line_chart(df[plot_cols])

except Exception as e:
    st.write("Erro ao carregar dados:", e)



# import streamlit as st
# import pandas as pd
# from streamlit_autorefresh import st_autorefresh

# CSV_FILE = 'dados_rede.csv'

# # Atualiza automaticamente a cada 5 segundos
# st_autorefresh(interval=5 * 1000, key="dashboard_autorefresh")

# st.title("Dashboard de Métricas da Rede")

# try:
#     # Lê CSV, ignora linhas ruins
#     df = pd.read_csv(CSV_FILE, on_bad_lines='skip')

#     # Verifica se a coluna timestamp existe
#     if 'timestamp' in df.columns:
#         df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
#         df = df.dropna(subset=['timestamp'])
#         df = df.set_index('timestamp')
#     else:
#         st.warning("Nenhuma coluna timestamp encontrada!")
#         # Cria índice temporário se não existir timestamp
#         df.index = range(len(df))

#     # Seleciona apenas as colunas que existem para plot
#     plot_cols = [c for c in ['RSSI', 'latencia_ms', 'perda_pct'] if c in df.columns]

#     if len(plot_cols) == 0:
#         st.warning("Nenhuma coluna de métricas encontrada!")
#     else:
#         st.subheader("Últimas métricas")
#         st.dataframe(df[plot_cols].tail(10))

#         st.line_chart(df[plot_cols])

# except Exception as e:
#     st.write("Erro ao carregar dados:", e)
