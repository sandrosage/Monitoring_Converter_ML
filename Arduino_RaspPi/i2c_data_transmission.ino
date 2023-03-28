#include <Wire.h>

#define DEV_ADDR 0x08
#define V_IN_ADDR 0x20
#define I_OUT_ADDR 0x22
#define V_OUT_ADDR 0x24
#define TEMP_ADDR 0x26
#define KHZ100 100000



byte x1, x2, x3, x4, x5, x6, x7, x8;
int cnt = 0;



void setup() {
  //switch it to 9600kps before 115200
  Serial.begin(115200);
  Wire.setClock(KHZ100); //
  Wire.begin();

}
void loop() {

  Wire.beginTransmission(DEV_ADDR);
  Wire.write(V_IN_ADDR);
  Wire.endTransmission();
  
  Wire.requestFrom(DEV_ADDR, 8);
  if (Wire.available()) {
    x1 = Wire.read();
    x2 = Wire.read();
    x3 = Wire.read();
    x4 = Wire.read();
    x5 = Wire.read();
    x6 = Wire.read();
    x7 = Wire.read();
    x8 = Wire.read();

    /*Serial.write(buf, len)*/
    byte buf[] = {x1, x2, x3, x4, x5, x6, x7, x8, '\r', '\n'};
    Serial.write(buf, sizeof(buf)); // write an array
    /*
    Serial.write(x1); //V first byte
    Serial.write(x2); //V second byte
    Serial.write(x3); //I first byte
    Serial.write(x4); //I second byte
    Serial.write(x5); //O first byte
    Serial.write(x6); //O second byte
    Serial.write(x7); //T first byte
    Serial.write(x8); //T second byte
    */
    /*delay(2);*/   /*problem: converter suddenly stops sending data (overload)*/
  }

}