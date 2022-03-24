#include <WiFi.h>
#include <WebServer.h>
#include <NewPing.h> //for Ultrasonic sensor
#include <PubSubClient.h> //for mqtt
#include <ArduinoJson.h>
#include <math.h>
#include <MPU9250.h>
#include "index.h"

const char* ssid = "true_home2G_8e2"; //Wifi SSID
const char* password = "82e568e2"; //Wifi Password

#define MQTT_SERVER "192.168.1.33" //mqtt server
#define MQTT_PORT 1883
#define MQTT_USERNAME "LINE"
#define MQTT_PASSWORD "FACEBOOK"
#define MQTT_NAME "CAR"

WebServer server(80);
WiFiClient espClient;
PubSubClient client(espClient);

DynamicJsonDocument doc(1024);
char buffer[256];
size_t n;

#define MOTORLEFT 36 //Encoder Motor Left Interrupt Pin
#define MOTORRIGHT 39 //Encoder Motor Right Interrupt Pin

int ps_values[2] = {0, 0}; //Counter Wheel count
int last_ps_values[2] = {0, 0}; //Store pervious counter wheel count
int diff;
float dist_values[2] = {0, 0};
float robot_pose[3] = {0, 0, 0};
static volatile unsigned long debouncel = 0;
static volatile unsigned long debouncer = 0;

int isMotorLeft_forward = 0;
int isMotorRight_forward = 0;

int counter_A = 0;
int counter_B = 0;

float v;
float w;
float vx;
float vy;

static float wheel_radius = 0.03;
static float distance_between_wheels = 0.11;
static float wheel_cirum = 2 * 3.14 * wheel_radius;
static float encoder_unit = wheel_cirum / 20; // meter per tick

static int dt = 1;

// Float for number of slots in encoder disk
float diskslots = 20;  // Change to match value of encoder disk

unsigned int defaultSpeed = 255;

int status = 0; // 0 - stop; 1 - forward; 2 - backward; 3 - left; 4 - right

MPU9250 mpu;

float gZ = 0;

//  Motor Left
#define LM_AV 27 // Left Motor Direction Pin - IN2
#define LM_AR 26 // Left Motor Speed Pin - IN1
#define LM_EN 25 // Left Enable Pin

//  Motor Right
#define RM_AV 12 // RIght Motor Direction Pin - IN3
#define RM_AR 14 // Right Motor Speed Pin - IN4
#define RM_EN 13 // Right Enable Pin

const int freq = 12800;
const int pwmChannelRight = 0;
const int pwmChannelLeft = 1;
const int resolution = 8;

#define SONAR_NUM 7 // Number of sensors.
#define MAX_DISTANCE 100 // Max distance in cm.

NewPing sonar[SONAR_NUM] = { //(Trigger,Echo)
  NewPing(2, 15, MAX_DISTANCE), //US_L1
  NewPing(16, 4, MAX_DISTANCE), //US_L2
  NewPing(5, 17, MAX_DISTANCE), //US_L3
  NewPing(19, 18, MAX_DISTANCE), //US_C
  NewPing(3, 23, MAX_DISTANCE), //US_R3
  NewPing(32, 34, MAX_DISTANCE), //US_R1
  NewPing(33, 35, MAX_DISTANCE) //US_R2
};

double CM[SONAR_NUM] = {0, 0, 0, 0, 0, 0, 0};

void moveBackMotorLeft(int speed) {
  digitalWrite(LM_AV, LOW);
  digitalWrite(LM_AR, HIGH);
  //analogWrite(LM_EN, speed);
  ledcWrite(pwmChannelLeft, speed);
}

void moveBackMotorRight(int speed) {
  digitalWrite(RM_AV, LOW);
  digitalWrite(RM_AR, HIGH);
  //analogWrite(RM_EN, speed);
  ledcWrite(pwmChannelRight, speed);
}

void moveBackward(int speedL, int speedR) {
  moveBackMotorLeft(speedL);
  moveBackMotorRight(speedR);
}

void moveForwardMotorLeft(int speed) {
  digitalWrite(LM_AV, HIGH);
  digitalWrite(LM_AR, LOW);
  //analogWrite(LM_EN, speed);
  ledcWrite(pwmChannelLeft, speed);
}

void moveForwardMotorRight(int speed) {
  digitalWrite(RM_AV, HIGH);
  digitalWrite(RM_AR, LOW);
  //analogWrite(RM_EN, speed);
  ledcWrite(pwmChannelRight, speed);
}

void stopMotorLeft() {
  digitalWrite(LM_AV, LOW);
  digitalWrite(LM_AR, LOW);
  //analogWrite(LM_EN, 0);
  ledcWrite(pwmChannelLeft, 0);
}

void stopMotorRight() {
  digitalWrite(RM_AV, LOW);
  digitalWrite(RM_AR, LOW);
  //analogWrite(RM_EN, 0);
  ledcWrite(pwmChannelRight, 0);
}

void stopMotor() {
  
  stopMotorLeft();
  stopMotorRight();
  
}

// steps Motor

void MoveForward(int speedL, int speedR) {

  isMotorLeft_forward = 1;
  isMotorRight_forward = 1;

  moveForwardMotorLeft(speedL);
  moveForwardMotorRight(speedR);

}

void MoveBackward(int speedL, int speedR) {

  isMotorLeft_forward = -1;
  isMotorRight_forward = -1;

  moveBackMotorLeft(speedL);
  moveBackMotorRight(speedR);
  
}

void turnLeft(int speedL, int speedR) {

  isMotorLeft_forward = -1;
  isMotorRight_forward = 1;

  moveBackMotorLeft(speedL);
  moveForwardMotorRight(speedR);

}

void turnRight(int speedL, int speedR) {

  isMotorLeft_forward = 1;
  isMotorRight_forward = -1;

  moveForwardMotorLeft(speedL);
  moveBackMotorRight(speedR);

}

void devicesMove() {

  int speedL = 0;
  int speedR = 0;
  int steps_direction = 0;
  
  if (server.hasArg("speedL")) {
    speedL = server.arg("speedL").toInt();
  }
  if (server.hasArg("speedR")) {
    speedR = server.arg("speedR").toInt();
  }
  if (server.hasArg("steps_direction")) {
    steps_direction = server.arg("steps_direction").toInt();
  }

  /* 0 - stop
   * 1 - left
   * 2 - backward
   * 3 - forward
   * 4 - right
   */

  if (steps_direction == 1) {
    turnLeft(speedL, speedR);
  } else if (steps_direction == 2) {
    MoveBackward(speedL, speedR);
  } else if (steps_direction == 3) {
    MoveForward(speedL, speedR);
  } else if (steps_direction == 4) {
    turnRight(speedL, speedR);
  } else {
    stopMotor();
  }

  server.send(200, "text/plain", "moveForwardSlow");
}

void devicesStop() {
  stopMotor();
  server.send(200, "text/plain", "moveStop");
}

void devicesResetEncoder() {
  stopMotor();
  
  ps_values[0] = 0;
  ps_values[1] = 0;
  last_ps_values[0] = 0;
  last_ps_values[1] = 0;
  robot_pose[0] = 0;
  robot_pose[1] = 0;
  robot_pose[2] = 0;
}

// Interrupt Service Routines

// Motor 1 pulse count ISR
void ISR_countLeft() {
  if (!digitalRead (MOTORLEFT) && (micros() - debouncel > 500) && !digitalRead (MOTORLEFT) ) {
    // Check again that the encoder sends a good signal and then check that the time is greater than 500 microseconds and check again that the signal is correct.
    debouncel = micros(); // Store the time to check that we do not count the rebound in the signal.
    //check if motor A pass next position
    if (isMotorLeft_forward == 1) {
        ps_values[0] = ps_values[0] + 1;
    } else if (isMotorLeft_forward == -1) {
        ps_values[0] = ps_values[0] - 1;
    }
}
  else ;
}

// Motor 2 pulse count ISR
void ISR_countRight() {
  if (!digitalRead (MOTORRIGHT) && (micros() - debouncel > 500) && !digitalRead (MOTORRIGHT) ) {
    debouncer = micros();
    // check if motor B pass next position
    if (isMotorRight_forward == 1) {
        ps_values[1] = ps_values[1] + 1;
    } else if (isMotorRight_forward == -1) {
        ps_values[1] = ps_values[1] - 1;
    }
}
  else ;
}

void handle_OnConnect() {
  String p = MAIN_page;
  server.send(200, "text/html", p);
}

void handle_NotFound() {
  server.send(404, "text/plain", "Not found");
}

void odemetry() {

  for (uint8_t i = 0; i < 2; i++) {
    diff = ps_values[i] - last_ps_values[i]; // Tick
    /*
    if (diff < 0.001) {
      diff = 0;
      ps_values[i] = last_ps_values[i];
    }
    */
    
    dist_values[i] = diff * encoder_unit; // Meter
  }

  v = (dist_values[0] + dist_values[1]) / 2.0;
  w = (dist_values[0] - dist_values[1]) / distance_between_wheels;

  robot_pose[2] += (w * dt); // w*dt

  vx = v * cos(robot_pose[2]);
  vy = v * sin(robot_pose[2]);

  robot_pose[0] += (vx * dt);
  robot_pose[1] += (vy * dt);

  last_ps_values[0] = ps_values[0];
  last_ps_values[1] = ps_values[1];
}

void packToMqtt() {
  doc["US_L1"] = CM[0];
  doc["US_L2"] = CM[1];
  doc["US_L3"] = CM[2];
  doc["US_C"] = CM[3];
  doc["US_R3"] = CM[4];
  doc["US_R2"] = CM[5];
  doc["US_R1"] = CM[6];
  doc["X"] = robot_pose[0];
  doc["Y"] = robot_pose[1];
  doc["theta"] = robot_pose[2];
  doc["L"] = ps_values[0];
  doc["R"] = ps_values[1];
  doc["T"] = millis();
  n = serializeJson(doc, buffer);
  client.publish("esp/test", buffer, n);
}

void setup() {
  pinMode(MOTORLEFT, INPUT);
  pinMode(MOTORRIGHT, INPUT);
  pinMode(LM_AV, OUTPUT);
  pinMode(LM_AR, OUTPUT);
  pinMode(LM_EN, OUTPUT);
  pinMode(RM_AV, OUTPUT);
  pinMode(RM_AR, OUTPUT);
  pinMode(RM_EN, OUTPUT);

  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  WiFi.begin(ssid, password);
  Serial.println("Connecting to Wifi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.println("");
  }
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  attachInterrupt(digitalPinToInterrupt (MOTORLEFT), ISR_countLeft, FALLING);  // Increase counter 1 when speed sensor pin goes High
  attachInterrupt(digitalPinToInterrupt (MOTORRIGHT), ISR_countRight, FALLING);  // Increase counter 2 when speed sensor pin goes High
  Serial.println("- Attach Interrupt");

  ledcSetup(pwmChannelRight, freq, resolution);
  ledcSetup(pwmChannelLeft, freq, resolution);

  ledcAttachPin(RM_EN, pwmChannelRight);
  ledcAttachPin(LM_EN, pwmChannelLeft);

  ledcWrite(pwmChannelLeft, 255);
  ledcWrite(pwmChannelRight, 255);
  Serial.println("- set motor speed: 100%");

  server.on("/", handle_OnConnect);
  server.on("/move", devicesMove);
  server.on("/stop", devicesStop);
  server.on("/reset", devicesResetEncoder);
  server.onNotFound(handle_NotFound);

  server.begin();
  Serial.println("HTTP server started");
  
  client.setServer(MQTT_SERVER, MQTT_PORT);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32Client", MQTT_USERNAME, MQTT_PASSWORD )) {
      Serial.println("connected");
    } else {
      Serial.print("Failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

int count = 0;
uint32_t prev_ms = millis();

void loop() {

  client.loop();
  server.handleClient();

  if (millis() > prev_ms + 33) {
    //Serial.print(count);
    //Serial.print("=");
    CM[count] = sonar[count].ping_cm();
    //Serial.print(CM[count]);
    //Serial.print("cm ");
    prev_ms = millis();
    count++;
    
    packToMqtt();

    if (count == 7) {
      count = 0;
    }
  
    odemetry();

    Serial.print("ps_values 0 : ");
    Serial.print(ps_values[0]);
    
    Serial.print("ps_values 0 : ");
    Serial.print(digitalRead (MOTORLEFT));

    Serial.print("ps_values 1 : ");
    Serial.print(ps_values[1]);
    
    Serial.print("ps_values 1 : ");
    Serial.print(digitalRead (MOTORRIGHT));
        
    Serial.println("");

  }

}