#include <ESP8266WiFi.h>
#include <LiquidCrystal.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_MLX90614.h>
const int PulseSensorHRWire = A0;
int Signal;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
const char* ssid = "Rivendol";
const char* password = "radoan151";
unsigned long lasttime = 0;
unsigned long timedelay = 5000;

void setup() {
  Serial.begin(9600);
  delay(10);
  
  Serial.println();
  Serial.println(); Serial.print("Connecting....");
  Serial.println(ssid);

//  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  if(WiFi.status() == WL_CONNECTED){
    Serial.println("Connected");
  }
  else{
    Serial.println("Not Connected");
  }
  Serial.println("Wifi Connected");
  Serial.println(WiFi.localIP());

  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor. Check wiring.");
    while (1);
  };
  

}

void loop() {
  if((millis() - lasttime) > timedelay){
    if(WiFi.status() == WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
      const char* server = "http://20.120.113.1/reports/";
      Signal = analogRead(PulseSensorHRWire);
      float bpm = ((Signal / 4) / 3.1);
      http.begin(client, server);
      http.addHeader("Content-Type","application/x-www-form-urlencoded");
      http.addHeader("Authorization","Token 3c17205ee7f50f4192d98fdc73c7d8384b1b5d2a");
      if(mlx.readAmbientTempC() != 0.0 && mlx.readObjectTempC() != 0.0 && mlx.readAmbientTempF() != 0.0){
        String requestData = "heart_rate="+String(bpm,2)+"&oxygen_level="+String(bpm,2)+"&temperature="+String(mlx.readAmbientTempF(),2);
        int dataCode = http.POST(requestData);
        lcd.setCursor (0,0);
        lcd.print("MyBPM:");
        lcd.setCursor(6,0);
        lcd.print(bmp);
        lcd.setCursor(0,1);
        lcd.print("Temp:  ");
        lcd.setCursor(6,1);
        lcd.print(mlx.readObjectTempF());
        http.end();
      }
      else{
        Serial.println("No Data");
      }
    }else{
      Serial.println("Wifi disconnected");
    }
  }
  delay(3000);
  

}
