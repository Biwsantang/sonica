// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#include <MPU9250_asukiaaa.h>
#include <ArduinoJson.h>

//right
#define echoPin_R 6
#define trigPin_R 7

//center
#define echoPin_C 4
#define trigPin_C 5

//left
#define echoPin_L 2
#define trigPin_L 3

MPU9250_asukiaaa mySensor;
float aX, aY, aZ, aSqrt, gX, gY, gZ, mDirection, mX, mY, mZ;

// defines variables
long duration_R,duration_C,duration_L; // variable for the duration of sound wave travel
int distance_R,distance_C,distance_L; // variable for the distance measurement

void setup() {
  pinMode(trigPin_R, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin_R, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPin_C, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin_C, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPin_L, OUTPUT);
  pinMode(echoPin_L, INPUT);

  Serial.begin(115200); // // Serial Communication is starting with 9600 of baudrate speed
  
  while (!Serial);

  mySensor.beginAccel();
  mySensor.beginGyro();
  mySensor.beginMag();
}
void loop() {
  digitalWrite(trigPin_L, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin_L, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin_L, LOW);
  duration_L = pulseIn(echoPin_L, HIGH);
  
  digitalWrite(trigPin_C, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin_C, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin_C, LOW);
  duration_C = pulseIn(echoPin_C, HIGH);

  digitalWrite(trigPin_R, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin_R, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin_R, LOW);
  duration_R = pulseIn(echoPin_R, HIGH);

  distance_R = duration_R * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  distance_C = duration_C * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  distance_L = duration_L * 0.034 / 2;

  if (mySensor.accelUpdate() == 0) {
    aX = mySensor.accelX();
    aY = mySensor.accelY();
    aZ = mySensor.accelZ();
    aSqrt = mySensor.accelSqrt();
/*    Serial.print("accelX: " + String(aX));
    Serial.print("\taccelY: " + String(aY));
    Serial.print("\taccelZ: " + String(aZ));
    Serial.print("\taccelSqrt: " + String(aSqrt));
*/  }

  if (mySensor.gyroUpdate() == 0) {
    gX = mySensor.gyroX();
    gY = mySensor.gyroY();
    gZ = mySensor.gyroZ();
 /*   Serial.print("\tgyroX: " + String(gX));
    Serial.print("\tgyroY: " + String(gY));
    Serial.print("\tgyroZ: " + String(gZ));
 */ }

  if (mySensor.magUpdate() == 0) {
    mX = mySensor.magX();
    mY = mySensor.magY();
    mZ = mySensor.magZ();
    mDirection = mySensor.magHorizDirection();
/*    Serial.print("\tmagX: " + String(mX));
    Serial.print("\tmaxY: " + String(mY));
    Serial.print("\tmagZ: " + String(mZ));
    Serial.print("\thorizontalDirection: " + String(mDirection));
*/  }

//  Serial.println(String(distance_L)+","+String(distance_C)+","+String(distance_R));

DynamicJsonDocument doc(1024);

  doc["ultra"][0] = distance_L;
  doc["ultra"][1] = distance_C;
  doc["ultra"][2] = distance_R;
  doc["accel"][0] = aX;
  doc["accel"][1] = aY;
  doc["accel"][2] = aZ;
  doc["accel"][3] = aSqrt;
  doc["gyro"][0] = gX;
  doc["gyro"][1] = gY;
  doc["gyro"][2] = gZ;
  doc["mag"][0] = mX;
  doc["mag"][1] = mY;
  doc["mag"][2] = mZ;
  doc["mag"][3] = mDirection;

serializeJson(doc, Serial);
    Serial.println("");
}
