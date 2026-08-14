
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Esme";
const char* password = "12345678";

String serverName = "http://10.1.1.69:5000/api/ultrasonic";

#define TRIG 5
#define ECHO 18

void setup() {
  Serial.begin(115200);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

float readDistance() {

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 30000);

  float distance = duration * 0.034 / 2;

  
  if (distance <= 0 || distance > 400) return -1;

  return distance;
}

void loop() {

  float distance = readDistance();

  if (distance != -1 && WiFi.status() == WL_CONNECTED) {

    String url = serverName +
      "?distance=" + String(distance);

    HTTPClient http;
    http.begin(url);
    http.GET();
    http.end();
  }

  delay(1000);
}
