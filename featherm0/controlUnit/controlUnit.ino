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

String serialData;

void setup() {
  serialData="";
  
  Serial.begin(9600);
  initJECCbot();

  DOG.begin(DIS_CS,0,0,DIS_A0,DIS_RESET,DOGM132);
  DOG.clear(); 

  pinMode(BACKLIGHTPIN, OUTPUT);
  digitalWrite(BACKLIGHTPIN, HIGH);

}

void loop() {

  updateJECCbot();
  
  char buffer[50];

  sprintf(buffer, "%04d", apiRegister.bench[REG_COMPASS_HEADING]);
  DOG.string(0, 0, UBUNTUMONO_B_16, buffer, ALIGN_LEFT);

  sprintf(buffer, "%03d %03d %03d", apiRegister.bench[REG_SONAR_LEFT], apiRegister.bench[REG_SONAR_MIDDLE], apiRegister.bench[REG_SONAR_RIGHT]);
  DOG.string(0, 2, UBUNTUMONO_B_16, buffer, ALIGN_LEFT);
}
  
void serialEventRun()
{
  if(Serial.available())
  {
    char c = Serial.read();
    serialData += c;
    if(c == '\n' && serialData.length() > 0)
    {   
        char *str = new char[serialData.length()+1];
        serialData.toCharArray(str, serialData.length()+1);
        Serial.flush();
        //locked = true;
        Serial.print(processCommand(str).message);
        free(str);
        //locked = false;
        serialData = "";
        Serial.flush();
    }
  }
}
