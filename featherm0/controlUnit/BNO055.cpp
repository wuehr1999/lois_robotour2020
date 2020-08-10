#include "BNO055.h"

void bno055Init(BNO055 *bno, int address, int phaseOffset)
{
  Wire.begin();

  bno->address = address;
  bno->phaseOffset = phaseOffset;
  //Serial.println(address);

  Wire.beginTransmission(bno->address);
  Wire.write(BNO055_REGISTER_OPMODE);
  Wire.write(BNO055_VALUE_OPMODE);
  Wire.endTransmission(false);
}

void bno055Update(BNO055 *bno)
{
  //Check opmode
  Wire.beginTransmission(bno->address);
  Wire.write(BNO055_REGISTER_OPMODE);
  Wire.endTransmission(false);
  Wire.requestFrom(bno->address, 1, true);
  byte opmode=Wire.read();
  if(opmode!=BNO055_VALUE_OPMODE)
  {
    Wire.beginTransmission(BNO055_ADDRESS);
    Wire.write(BNO055_REGISTER_OPMODE);
    Wire.write(BNO055_VALUE_OPMODE);
    Wire.endTransmission(false);
  }

  //Read calibraion
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(BNO055_REGISTER_CALIBSTAT);
  Wire.endTransmission(false);
  Wire.requestFrom(BNO055_ADDRESS, 4, true);
  byte mag=Wire.read();
  byte acc=Wire.read();
  byte gyr=Wire.read();
  byte sys=Wire.read();

  bno->mag=(int)((float)mag/2.55);
  bno->acc=(int)((float)acc/2.55);
  bno->gyr=(int)((float)gyr/2.55);
  bno->sys=(int)((float)sys/2.55);

  bno->calibStat=(bno->mag+bno->acc+bno->gyr+bno->sys)/4;
  
  //Read heading
  Wire.beginTransmission(bno->address);
  Wire.write(BNO055_REGISTER_HEADING);  
  Wire.endTransmission(false);
  Wire.requestFrom(bno->address, 2, true);
  byte b1=Wire.read();
  byte b2=Wire.read();
  Wire.endTransmission(false);
  uint16_t rawHeading=(b2<<8)|b1;
  int heading=(int)((float)rawHeading/16.0) + bno->phaseOffset;

  if(heading > 360)
  {
    heading = heading - 360;
  }
  
  if(heading>180)
  {
    heading=heading-360;
  }
  
  bno->heading=heading;  
}
