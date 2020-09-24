/**
 * 
 * 
 *
 */

/* import libraries */
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

/* set ssid and and password */
const char *ssid = "SecuritySystem"; 
const char *password = "thereisnospoon";

String htmlPage = "Some html"; //TODO

int waitingTime = 100;
int counter = 0;
int ledPin = 5;
int sensorUpdates = 10; //TODO

boolean ledState = true;

ESP8266WebServer server(80);

/* Just a little test message.  Go to http://192.168.4.1 in a web browser
   connected to this access point to see it.
*/
void handleRoot() {
  server.send(200, "text/html", "<h1>You are connected</h1>");
}

void setup() {
  delay(1000);
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  
  Serial.println();
  Serial.println("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid/*, password*/);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("IP address: ");
  Serial.println(myIP);
  Serial.print("ssid: ");
  Serial.println(ssid);
  Serial.print("password: ");
  Serial.println(password);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  counter++;
  ledState = !ledState;

  if (sensorUpdates == counter){
    //sensorUpdate
    counter = 0;
    
    Serial.println(String(ledState));
    if (ledState == true){
      digitalWrite(ledPin, HIGH);
    }
    else if (ledState == false){
      digitalWrite(ledPin, LOW);
    }
  }
  
  Serial.println("updating server to: " + "<h1>You are connected " + String(counter) + "<br>" + "Led status" + String(ledState) + "</h1>");
  server.send(200, "text/html", "<h1>You are connected " + String(counter) + "<br>" + "Led status " + String(ledState) + "</h1>");
  
  server.handleClient();
  delay(waitingTime);
}
