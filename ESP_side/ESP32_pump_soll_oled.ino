#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <string.h>
#include <ArduinoJson.h>


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino resetpin)

const int SOLL_PIN = 34; // soil sensor pin
const int LED_GREEN = 23;
const int LED_RED = 19;
const int PUMP_PIN = 4;
const int OpenAirReading = 3031;   //calibration data 1
const int WaterReading = 1735;     //calibration data 2

const char* ssid ="TemplateSSID";
const char* password ="YOURPASSWORD";

int MoistureLevel = 0;
int SoilMoisturePercentage = 0;
int time1 = 1; // time in mins
int time2 = time1*60*1000; // delay post

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

StaticJsonDocument<200> doc;

///connect to internet
void Connect_internet()
{
  Serial.println("");
  Serial.print("Connecting to: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    digitalWrite(LED_RED, HIGH);
    delay(200);
    digitalWrite(LED_RED, LOW);
    delay(300);
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
}

void show(String message){
  display.clearDisplay();
  display.fillScreen(BLACK);
  display.display();
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 8);
  display.println(message); //avg
  display.display();
}

void setup() {
  Serial.begin(115200);
  Serial.println("INIT SETUP");
  pinMode(SOLL_PIN, INPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);  
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }
  display.setTextColor(WHITE);
  display.setTextWrap(false);
  delay(10);
  Serial.println("SETUP COMPLETE");
}

void loop() {
  Serial.println("INIT LOOP");
  if (WiFi.status() != WL_CONNECTED) {
    show("CONNECTING");
    Connect_internet();
  }else
  {
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {
    MoistureLevel = analogRead(SOLL_PIN);  //update based on the analog Pin selected
    Serial.println("Analog moisture level: ");
    Serial.println(MoistureLevel);
    SoilMoisturePercentage = map(MoistureLevel, OpenAirReading, WaterReading, 0, 100);
    if (SoilMoisturePercentage < 0) SoilMoisturePercentage = 0;
    else if(SoilMoisturePercentage > 100) SoilMoisturePercentage = 100;
    Serial.println("Percent moisture level: ");
    Serial.println(SoilMoisturePercentage);

    String input = "{\"HUMIDITY\":";
    input+= SoilMoisturePercentage;
    input += "}";
    
    WiFiClient client;
    HTTPClient http_post;
    HTTPClient http_get;

    Serial.print("[HTTP] POST begin...\n");
    // configure traged server and url
    http_post.begin(client, "http://192.168.43.205:80/snippets/");  // HTTP  SERVER_IP "/postplain/"
    http_post.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body
    int postResponse = http_post.POST(input);
    
    // httpCode will be negative on error
    if(postResponse>0)
    {
      Serial.printf("[HTTP] POST... code: %d\n", postResponse);
      if (postResponse == 201){
        Serial.println("POST successfull");
        digitalWrite(LED_GREEN, HIGH);   
        delay(1000);     
        digitalWrite(LED_GREEN, LOW);

        Serial.print("[HTTP] GET begin...\n");
        // configure traged server and url
        http_get.begin(client, "http://192.168.43.205:80/get_average/");  // HTTP  SERVER_IP "/postplain/"
        http_get.addHeader("Content-Type", "application/json");
        Serial.print("[HTTP] GET...\n");
        // start connection and send HTTP header and body
        int getResponse = http_get.GET();
        String json_data = http_get.getString();
        Serial.println(json_data);
        // Deserialize the JSON document
        DeserializationError error = deserializeJson(doc, json_data.c_str());
        if (error) {
          Serial.print(F("deserializeJson() failed: "));
          Serial.println(error.f_str());
          return;
        }
        long avg_hum = doc["avg_hum"];
        Serial.println(avg_hum);
        long pump_flag = doc["pump_flag"];
        Serial.println(pump_flag);
        String disp_mes = " HUM: " + String(avg_hum) + "%";

        Serial.printf("[HTTP] GET... code: %d\n", getResponse);
        if (pump_flag){
          Serial.println("Pumping start...");
          show(" WATERING");
          digitalWrite(PUMP_PIN, LOW);
          delay(5000);
          digitalWrite(PUMP_PIN, HIGH);
          Serial.println("Pumping end");
        }
        show(disp_mes.c_str());
      } else
      {
        Serial.printf("[HTTP] POST... failed, error: %s\n", http_post.errorToString(postResponse).c_str());
      }
    }
    http_get.end();  //Free resources
    http_post.end();  //Free resources
  }    
  delay(time2);
  }
}