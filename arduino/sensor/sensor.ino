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

// defines variables
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
  mpu.verbose(true);
  delay(5000);
  mpu.calibrateAccelGyro();

  Serial.println("Mag calibration will start in 5sec.");
  Serial.println("Please Wave device in a figure eight until done.");
  delay(5000);
  mpu.calibrateMag();

  print_calibration();
  mpu.verbose(false);

}
void loop() {

  if (mpu.update()) {
        static uint32_t prev_ms = millis();
        if ((millis() - prev_ms) > 100) {
            doc["rotation"][0] = (float)mpu.getRoll();
            doc["rotation"][1] = (float)mpu.getPitch();
            doc["rotation"][2] = (float)mpu.getYaw();

            //doc["accel"][0] = mpu.getAccX();
            //doc["accel"][1] = mpu.getAccY();
            //doc["accel"][2] = mpu.getAccZ();

            prev_ms = millis();
        }

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

        doc["ultra"][2] = (int)duration_R * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
        doc["ultra"][1] = (int)duration_C * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
        doc["ultra"][0] = (int)duration_L * 0.034 / 2;
    }

  serializeJson(doc, Serial);
  Serial.println("");

}

void print_calibration() {
  Serial.println("< calibration parameters >");
  Serial.println("accel bias [g]: ");
  Serial.print(mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.println();
  Serial.println("gyro bias [deg/s]: ");
  Serial.print(mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.println();
  Serial.println("mag bias [mG]: ");
  Serial.print(mpu.getMagBiasX());
  Serial.print(", ");
  Serial.print(mpu.getMagBiasY());
  Serial.print(", ");
  Serial.print(mpu.getMagBiasZ());
  Serial.println();
  Serial.println("mag scale []: ");
  Serial.print(mpu.getMagScaleX());
  Serial.print(", ");
  Serial.print(mpu.getMagScaleY());
  Serial.print(", ");
  Serial.print(mpu.getMagScaleZ());
  Serial.println();
}
