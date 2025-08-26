#include <WiFi.h>
#include <ESP32Ping.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>  // necessário para POST HTTP
#include "config.h" // inclua credenciais separadas



IPAddress remote_ip(192,168,1,14);  // IP do servidor para teste de ping

// Função para montar JSON e enviar
void enviarMetricas(int rssi, float latencia, float perda_pct) {
  StaticJsonDocument<200> doc;
  doc["RSSI"] = rssi;
  doc["latencia_ms"] = latencia;
  doc["perda_pct"] = perda_pct;

  String payload;
  serializeJson(doc, payload);

  Serial.println("[DEBUG] JSON Gerado: " + payload);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.printf("[DEBUG] POST -> Código HTTP: %d\n", httpResponseCode);
      String resposta = http.getString();
      Serial.println("[DEBUG] Resposta servidor: " + resposta);
    } else {
      Serial.printf("[ERRO] Falha no POST. Código: %d\n", httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("[ERRO] Wi-Fi não está conectado no momento do POST.");
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

  Serial.println("\nConectado ao Wi-Fi!");
  Serial.print("Endereço IP ESP32: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    int pacotes = 5, recebidos = 0;
    float soma_latencia = 0;

    Serial.println("\n--- Testando conexão ---");

    for (int i = 0; i < pacotes; i++) {
      if (Ping.ping(remote_ip, 1)) {
        recebidos++;
        float tempo = Ping.averageTime();
        soma_latencia += tempo;
        Serial.printf("Ping %d: %.2f ms\n", i+1, tempo);
      } else {
        Serial.printf("Ping %d: falhou\n", i+1);
      }
      delay(1000);
    }

    int perdidos = pacotes - recebidos;
    float perda_pct = (float)perdidos / pacotes * 100.0;
    float latencia_media = recebidos > 0 ? soma_latencia / recebidos : -1;
    int rssi = WiFi.RSSI();

    Serial.printf("Resumo -> Enviados: %d | Recebidos: %d | Perda: %.1f %% | Latência média: %.2f ms | RSSI: %d dBm\n",
                  pacotes, recebidos, perda_pct, latencia_media, rssi);

    enviarMetricas(rssi, latencia_media, perda_pct);

  } else {
    Serial.println("[ERRO] Wi-Fi desconectado, tentando reconectar...");
    WiFi.reconnect();
  }

  delay(10000);
}
