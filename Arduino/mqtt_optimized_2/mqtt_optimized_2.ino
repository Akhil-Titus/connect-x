#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// WiFi
const char *ssid = "akhiltitus";
const char *password = "akhiltitus";

// MQTT Broker
const char *mqtt_broker = "10.42.0.1";
const int mqtt_port = 1883;
const char *topic = "topicx";

WiFiClient espClient;
PubSubClient client(espClient);

Servo myservo1;
Servo myservo2;
String received_DATA = "";
String motor;
int angle;


void setup() {
  Serial.begin(115200);
 
  myservo1.attach(33);
  myservo2.attach(32);


  // Connecting to WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to the WiFi network");

  // Connecting to MQTT broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());

    Serial.printf("The client %s connects to MQTT broker\n", client_id.c_str());

    if (client.connect(client_id.c_str())) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }

  // Subscribe to the MQTT topic
  client.subscribe(topic);
}

void loop() {
  client.loop();
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message: ");
  Serial.println(message);

    // Extract motorX and motorY values from the message
  int motorX = 0;
  int motorY = 0;
 
  received_DATA = message.substring(1, (message.length() - 1));
  on_receive();

}
void on_receive(){
  motor = received_DATA.substring(0,1);
  angle = received_DATA.substring(1,received_DATA.length()).toInt();

  if (motor == "X"){
    myservo1.write(angle);
    Serial.print("motorX: ");
    Serial.println(angle);
    
  }
  if (motor == "Y"){
    myservo2.write(angle);
    Serial.print("motorY: ");
  Serial.println(angle);
  }
}
