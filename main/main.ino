#include <WiFi.h>
#include <ESP32Ping.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include <time.h>
// Endereço do servidor Flask


IPAddress remote_ip(192,168,1,14);


// NTP
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -10800; // GMT-3
const int daylightOffset_sec = 0;

// Função para obter timestamp
String getTimestamp() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    return "0000-00-00 00:00:00";
  }
  char buffer[20];
  strftime(buffer, 20, "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(buffer);
}

// Função para montar e imprimir JSON
void enviarMetricas(const String& ssid_nome, const String& bssid, int canal, const String& ip_local,
                     int rssi, float latencia, float perda_pct, int enviados, int recebidos, float taxa_sucesso) {

  String timestamp = getTimestamp();

  StaticJsonDocument<400> doc;
  doc["timestamp"] = timestamp;
  doc["SSID"] = ssid_nome;
  doc["BSSID"] = bssid;
  doc["canal"] = canal;
  doc["IP_local"] = ip_local;
  doc["RSSI"] = rssi;
  doc["latencia_ms"] = latencia;
  doc["perda_pct"] = perda_pct;
  doc["pacotes_enviados"] = enviados;
  doc["pacotes_recebidos"] = recebidos;
  doc["taxa_sucesso_pct"] = taxa_sucesso;

  String output;
  serializeJson(doc, output);
  Serial.println("JSON Gerado: " + output);

  // Aqui você pode enviar via HTTP POST para o Flask se quiser
  
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type","application/json");
    int code = http.POST(output);
    Serial.println("HTTP POST code: " + String(code));
    http.end();
  }
  
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("Iniciando conexão Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.print("Endereço IP: "); Serial.println(WiFi.localIP());
  Serial.print("SSID Conectado: "); Serial.println(WiFi.SSID());
  Serial.print("RSSI (força do sinal): "); Serial.println(WiFi.RSSI());

  // Configura NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("Sincronizando hora...");
  struct tm timeinfo;
  while(!getLocalTime(&timeinfo)){
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nHora sincronizada!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    int pacotes = 10;
    int recebidos = 0;
    float soma_latencia = 0;

    Serial.println("\n--- Testando conexão ---");

    for (int i = 0; i < pacotes; i++) {
      if (Ping.ping(remote_ip, 1)) {
        recebidos++;
        float tempo = Ping.averageTime();
        soma_latencia += tempo;
        Serial.print("Ping "); Serial.print(i + 1); Serial.print(": "); Serial.print(tempo); Serial.println(" ms");
      } else {
        Serial.print("Ping "); Serial.print(i + 1); Serial.println(": falhou");
      }
      delay(1000);
    }

    int perdidos = pacotes - recebidos;
    float perda_pct = (float)perdidos / pacotes * 100.0;
    float latencia_media = recebidos > 0 ? soma_latencia / recebidos : -1;
    int rssi = WiFi.RSSI();
    float taxa_sucesso = recebidos > 0 ? ((float)recebidos / pacotes) * 100.0 : 0.0;

    Serial.print("Pacotes enviados: "); Serial.println(pacotes);
    Serial.print("Pacotes recebidos: "); Serial.println(recebidos);
    Serial.print("Perda de pacotes: "); Serial.print(perda_pct); Serial.println(" %");
    Serial.print("Taxa de sucesso: "); Serial.print(taxa_sucesso); Serial.println(" %");

    // Envia métricas
    enviarMetricas(WiFi.SSID(), WiFi.BSSIDstr(), WiFi.channel(), WiFi.localIP().toString(),
                    rssi, latencia_media, perda_pct, pacotes, recebidos, taxa_sucesso);

    // Debug: mostrando servidor
    Serial.print("Enviando métricas para: "); Serial.println(serverName);
  } else {
    Serial.println("Wi-Fi desconectado, tentando reconectar...");
    WiFi.reconnect();
  }

  delay(10000); // espera 10s antes do próximo teste
}