/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <ESP8266WiFi.h>
#include "RestClient.h"

const char* ssid     = "uaifi";
const char* password = "adm020311";

const char* host = "data.sparkfun.com";

void WiFiEvent(WiFiEvent_t event) {
//    Serial.printf("[WiFi-event] event: %d\n", event);

    switch(event) {
        case WIFI_EVENT_STAMODE_GOT_IP:
            Serial.println("");
            Serial.println("WiFi connected");
            Serial.println("IP address: ");
            Serial.println(WiFi.localIP());
            Serial.println("");
            break;
        case WIFI_EVENT_STAMODE_DISCONNECTED:
            Serial.println("WiFi lost connection");
            break;
    }
}

void setup() {
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  // delete old config
  WiFi.disconnect(true);
  delay(200);

  WiFi.onEvent(WiFiEvent);

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
}

int value = 0;

String response;
int statusCode;

RestClient rest_client = RestClient("httpbin.org");

void loop() {
  delay(1000);

  response = "";
  Serial.println("-------- get --------");
  statusCode = rest_client.get("/get", &response);
  Serial.print("Status code from server: ");
  Serial.println(statusCode);
  Serial.print("Response body from server: ");
  Serial.println(response);

  response = "";
  Serial.println("-------- get --------");
  statusCode = rest_client.get("/geta", &response);
  Serial.print("Status code from server: ");
  Serial.println(statusCode);
  Serial.print("Response body from server: ");
  Serial.println(response);
}

