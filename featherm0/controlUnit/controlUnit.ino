#include <Arduino.h>
#include <Wire.h>
#include <DogGraphicDisplay.h>
#include "ubuntumono_b_16.h"
#include "JECCbotAPI.h"

DogGraphicDisplay DOG;

#define BACKLIGHTPIN 13
#define EMERGENCYSTOP 18
#define DIS_CS 15
#define DIS_A0 17
#define DIS_RESET 16

void setup() {
  
  Serial.begin(115200);
  initJECCbot();

  pinMode(BACKLIGHTPIN,  OUTPUT);   // set backlight pin to output
  digitalWrite(BACKLIGHTPIN,  HIGH);  // enable backlight pin
  DOG.begin(DIS_CS,0,0,DIS_A0,DIS_RESET,DOGM132);
  DOG.clear(); 

  Serial.print(processCommand(":04004103ff\n").message);
  Serial.print(processCommand(":040042000f\n").message);
  Serial.print(processCommand(":0400000001\n").message);
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
  
  char buffer[50];
  sprintf(buffer, "%04d", apiRegister.bench[REG_COMPASS_HEADING]);
  DOG.string(0, 0, UBUNTUMONO_B_16, buffer, ALIGN_LEFT);

  
}
