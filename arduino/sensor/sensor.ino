#include <MPU9250.h>
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

MPU9250 mpu;

DynamicJsonDocument doc(128);

float gX,gY,gZ,u0,u1,u2;

long duration_R,duration_C,duration_L; // variable for the duration of sound wave travel

void setup() {

  pinMode(trigPin_R, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin_R, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPin_C, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin_C, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPin_L, OUTPUT);
  pinMode(echoPin_L, INPUT);

  Serial.begin(115200); // // Serial Communication is starting with 9600 of baudrate speed

  Wire.begin();
  delay(2000);

  if (!mpu.setup(0x68)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
  }

  // calibrate anytime you want to
  Serial.println("Accel Gyro calibration will start in 5sec.");
  Serial.println("Please leave the device still on the flat plane.");
  delay(5000);
  mpu.calibrateAccelGyro();

  Serial.println("Mag calibration will start in 5sec.");
  Serial.println("Please Wave device in a figure eight until done.");
  delay(5000);
  mpu.calibrateMag();
  Serial.println("Calibration finish");

}
void loop() {

  doc.clear();

  if (mpu.update()) {
    static uint32_t prev_ms = millis();
    if (millis() > prev_ms + 25) {

      gX = (float)mpu.getRoll();
      gY = (float)mpu.getPitch()*-1;
      gZ = (float)mpu.getYaw()*-1;

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

      u0 = duration_R * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
      u1 = duration_C * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
      u2 = duration_L * 0.034 / 2;

      doc.add(u0);
      doc.add(u1);
      doc.add(u2);
      doc.add(gX);
      doc.add(gY);
      doc.add(gZ);

      serializeJson(doc, Serial);
      Serial.println("");

      prev_ms = millis();

    }

  }

}
