//libraries
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Hash.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

const char* ssid     = "SecuritySystem";
const char* password = "<p>test</p>";

char laserStatus[] = "Good";
char htmlPage[] = "";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// unsigned long becouse time will get to long after time for an int to hold
unsigned long previousMillis = 0;    // will store last time DHT was updated

// Updates DHT readings every 10 seconds
const long updateInterval = 10000;

void setup(){
  delay(1000);
  // set serial monitor to 115200 baud
  Serial.begin(115200);
  
  Serial.println();
  Serial.println("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the Access Point to be open
  WiFi.softAP(ssid/*, password*/);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  // Print ESP8266 Local IP Address
  Serial.println(WiFi.localIP());

  // web page
  server.on("/laser status", HTTP_GET, [](AsyncWebServerRequest *request){request->send_P(200, "text/plain", String(laserStatus).c_str());});

  // Start server
  server.begin();
}
 
void loop(){  
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= updateInterval) {
    previousMillis = currentMillis;
    
  
  //TODO change motor variable
  }
}
