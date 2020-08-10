#include "JECCbotAPI.h"

#include <Arduino.h>
#include <Wire.h>

void setup() {
  
  Serial.begin(115200);
  initJECCbot();
}

void loop() {
  
  static String serialData = "";
  
  if(Serial.available())
  {
    char c = Serial.read();
    serialData += c;
    if(c == '\n')
    {      

      char *str = new char[serialData.length()+1];
      serialData.toCharArray(str, serialData.length()+1);
      Serial.print(processCommand(str).message);
      serialData = "";
    }
  }

  updateJECCbot();
}
