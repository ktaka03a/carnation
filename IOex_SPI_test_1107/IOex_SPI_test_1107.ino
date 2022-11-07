#include <SPI.h>
#include "MCP23S17.h"
#include <Servo.h>
#include <Wire.h>

MCP chip0(0, 10);
MCP chip1(1, 10);
MCP chip2(2, 10);
MCP chip3(3, 10);
Servo s;
int magnifier = 40;

void loop() {
  if (Serial.available()) {
    int count = 0;
    while (Serial.available()) {
      int offset = 0;
      int data = Serial.read();
      if (byte(data) != 128 and data != -1) {
        data = byte(data);
        int offset = 27;
        if (data > 127) {
          data = abs(128 - data);
          offset = 0;
        }
        dwrite(count + offset);
        delay(data * magnifier);
        dwrite(-1);
        delay(100);
      }
      else break;
      dwrite(-1);
      count++;
    }
    dwrite(-1);
    delay(100);
  }
  else {
    //    for(int i=0;i<54;i++){
    //      dwrite(i);
    //      delay(100);
    //    }
    dwrite(-1);
  }
  delay(1000);
}

void setup() {
  Serial.begin(9600);
//  Wire.begin();
  chip0.begin();
  chip1.begin();
  chip2.begin();
  chip3.begin();
  for (int i = 0; i <= 16; i++) {
    chip0.pinMode(i, OUTPUT);
    chip1.pinMode(i, OUTPUT);
    chip2.pinMode(i, OUTPUT);
    chip3.pinMode(i, OUTPUT);
  }
  dwrite(-1);
  s.attach(9);
  s.write(89);
}

void dwrite(int input) {
  static int mapping[] = {
    1, 0, 2, 16, 26, 17, 13, 28, 12, 9, 11, 19, 18, 4, 3, 10, 27, 23, 24, 25, 20, 22, 7, 21, 6, 8, 5,
    53, 54, 45, 44, 49, 60, 32, 48, 55, 58, 59, 50, 43, 51, 34, 33, 35, 57, 56, 40, 39, 36, 38, 42, 37, 41, 52
  };
  int j = mapping[input];
  for (int i = 0; i <= 16; i++) {
    chip0.digitalWrite(i, LOW);
    chip1.digitalWrite(i, LOW);
    chip2.digitalWrite(i, LOW);
    chip3.digitalWrite(i, LOW);
  }
  if (j == -1)return;
  else if (j < 16)    chip0.digitalWrite(16 - (j + 1), HIGH);
  else if (j < 32)    chip1.digitalWrite(16 - (j + 1 - 16), HIGH);
  else if (j < 48)    chip2.digitalWrite(16 - (j + 1 - 32), HIGH);
  else if (j < 64)    chip3.digitalWrite(16 - (j + 1 - 48), HIGH);
}
