#include "HWDriver.h"

Motor motorLeft, motorRight;
//BNO055 bno055;
KVHC100 kvhc100;

SonarExtenderI2C sonar;

void HWInit()
{
  motorInit(&motorLeft, MOT1_1, MOT1_2, MOT1_EN, MOT_FREQ, 16000);
  motorInit(&motorRight, MOT2_1, MOT2_2, MOT2_EN, MOT_FREQ, 16000);

  motorEnable(&motorLeft, 1);
  motorEnable(&motorRight, 1);

  pinMode(EM_STOP, INPUT);

  kvhc100Init(&kvhc100, KVH_PHASE_OFFSET);

  start1000Hz();
  start16000Hz();

  sonar.begin();
}

void changeMotorPwmFrequency(int pwmFrequency)
{
  motorChangePwmFrequency(&motorLeft, pwmFrequency);
  motorChangePwmFrequency(&motorRight, pwmFrequency);
}

void setMotors(int speedLeft, int speedRight)
{
  motorSetSpeed(&motorLeft, speedLeft);
  motorSetSpeed(&motorRight, speedRight);
}


void interrupt1000Hz()
{
  
}

void interrupt16000Hz()
{
  motorUpdate(&motorLeft);
  motorUpdate(&motorRight);
}

int getHeading()
{

  kvhc100Update(&kvhc100);
  return kvhc100.heading;
}

int getEmergencyStop()
{
  return digitalRead(EM_STOP);
}

int getSonar(uint8_t number)
{
  sonar.read(number);
  
  return sonar.getMeasurementCm(number);
}
