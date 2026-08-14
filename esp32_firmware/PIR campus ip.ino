#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ------------------------------------
// LCD SETUP
// ------------------------------------
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ------------------------------------
// WIFI SETTINGS
// ------------------------------------
const char* ssid = "Esme";
const char* password = "12345678";

// Flask endpoint
String server = "http://10.1.1.69:5000/api/pir";

// ------------------------------------
// PIR SENSOR
// ------------------------------------
#define PIR_PIN 13

int motionStatus = 0;

unsigned long lastSend = 0;
const int sendInterval = 2000;

// ------------------------------------
// SEND DATA FUNCTION
// ------------------------------------
void sendData(int motion) {

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    http.begin(server);

    http.addHeader("Content-Type", "application/json");

    // JSON OBJECT
    StaticJsonDocument<200> doc;

    doc["motion"] = motion;

    String jsonString;

    serializeJson(doc, jsonString);

    Serial.println("Sending JSON:");
    Serial.println(jsonString);

    int httpResponseCode = http.POST(jsonString);

    Serial.print("HTTP Response: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {

      String response = http.getString();

      Serial.println("Server Response:");
      Serial.println(response);
    }
    else {

      Serial.print("POST Error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }
  else {

    Serial.println("WiFi disconnected");
  }
}

void setup() {

  Serial.begin(115200);

  // ------------------------------------
  // PIR SETUP
  // ------------------------------------
  pinMode(PIR_PIN, INPUT);

  // ------------------------------------
  // LCD SETUP
  // ------------------------------------
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0,0);
  lcd.print("Greenhouse");

  lcd.setCursor(0,1);
  lcd.print("System Start");

  delay(2000);

  lcd.clear();

  // ------------------------------------
  // WIFI CONNECTION
  // ------------------------------------
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("WiFi Connected");

  delay(2000);
}

void loop() {

  // ------------------------------------
  // READ PIR SENSOR
  // ------------------------------------
  motionStatus = digitalRead(PIR_PIN);

  // ------------------------------------
  // SERIAL + LCD OUTPUT
  // ------------------------------------
  if (motionStatus == HIGH) {

    Serial.println("Motion Detected!");

    lcd.clear();

    lcd.setCursor(0,0);
    lcd.print("Motion Detected");

    lcd.setCursor(0,1);
    lcd.print("PIR ACTIVE");
  }

  else {

    Serial.println("No Motion");

    lcd.clear();

    lcd.setCursor(0,0);
    lcd.print("No Motion");

    lcd.setCursor(0,1);
    lcd.print("System Normal");
  }

  // ------------------------------------
  // SEND TO FLASK SERVER
  // ------------------------------------
  if (millis() - lastSend > sendInterval) {

    lastSend = millis();

    sendData(motionStatus);
  }

  delay(1000);
}
