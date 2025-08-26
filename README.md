# Sistema de Monitoramento de Rede com ESP32

Este projeto coleta métricas de Wi-Fi (RSSI, latência e perda de pacotes) com ESP32, envia para um servidor Flask e exibe em um dashboard Streamlit.

## Como usar

1. Crei e Configure `config.h` com seu Wi-Fi e IP do servidor.

```c++
#ifndef CONFIG_H
#define CONFIG_H

const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";

const char* serverName = "http://192.168.1.14:5000/metrics"; // IP do servidor Flask

#endif
```


2. Carregue `main.ino` no ESP32.
3. Rode o servidor Flask:
   ```bash
   python server.py
   ```

4. Rode o dashboard
  ```bash
  streamlit run dashboard.py
   ```

