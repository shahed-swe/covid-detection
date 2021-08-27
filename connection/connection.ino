#include <ESP8266WiFi.h>
#include <LiquidCrystal.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_MLX90614.h>


Adafruit_MLX90614 mlx = Adafruit_MLX90614();
const char* ssid = "Rivendol";
const char* password = "radoan151";
unsigned long lasttime = 0;
unsigned long timedelay = 5000;

void setup() {
  Serial.begin(9600);
  delay(10);
  int signal = analogRead(A0);
  float bpm = ((signal/4)/3.1);
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
      const char* server = "http://192.168.0.103/reports/";
      http.begin(client, server);
      http.addHeader("Content-Type","application/x-www-form-urlencoded");
      http.addHeader("Authorization","Token ac0308a6bbe5e5592e4ef8fa76f6ec95a003ddb4");
      if(mlx.readAmbientTempC() != 0.0 && mlx.readObjectTempC() != 0.0 && mlx.readAmbientTempF() != 0.0){
        String requestData = "heart_rate="+String(bpm,2)+"&oxygen_level="+String(bpm,2)+"&temperature="+String(mlx.readAmbientTempF(),2);
        int dataCode = http.POST(requestData);
        Serial.print("My BPM= "); Serial.println(bpm);
        Serial.println(mlx.readObjectTempF());
        Serial.print("HTTp Response Code:");
        Serial.println(String(dataCode));
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
