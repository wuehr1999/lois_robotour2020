#ifndef BNO055_H
#define BNO055_H

#include <Arduino.h>
#include <Wire.h>

#define BNO055_ADDRESS 0x29
#define BNO055_REGISTER_OPMODE 0x3d
#define BNO055_VALUE_OPMODE 0x0c
#define BNO055_REGISTER_CALIBSTAT 0x35
#define BNO055_REGISTER_HEADING 0x1a

/***Struct for storing BNO055 data***/
typedef struct BNO055{
  int address;
  int calibStat; //0-100%
  int sys; //0-100%
  int gyr; //0-100%
  int acc; //0-100%
  int mag; //0-100%

  int phaseOffset; // 0 to 180 degrees
  
  int heading; //-180 to 180 degrees
}BNO055;

/***Inits BNO with correct opmode***/
void bno055Init(BNO055 *bno, int address, int phaseOffset);

/***Updates BNO Data struct***/
void bno055Update(BNO055 *bno);

#endif
