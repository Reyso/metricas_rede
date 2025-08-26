# Sistema de Monitoramento de Rede com ESP32

Este projeto coleta métricas de Wi-Fi (RSSI, latência e perda de pacotes) com ESP32, envia para um servidor Flask e exibe em um dashboard Streamlit.

## Como usar

0. Recomenda-se criar um ambiente virtual.

1. Instale as dependências
 ```bash
   pip install -r requirements.txt
 ```

3. Crei e Configure `config.h` com seu Wi-Fi e IP do servidor.

```c++
#ifndef CONFIG_H
#define CONFIG_H

const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";

const char* serverName = "http://192.168.1.14:5000/metrics"; // IP do servidor Flask

#endif
```


3. Carregue `main.ino` no ESP32.
4. Rode o servidor Flask:
   ```bash
   python server.py
   ```

5. Rode o dashboard
  ```bash
  streamlit run dashboard.py
   ```

