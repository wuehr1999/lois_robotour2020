#ifndef HW_DRIVER_H
#define HW_DRIVER_H

#include <Arduino.h>

#include "Timers.h"
#include "Motor.h"
//#include "BNO055.h"
#include <SonarExtenderI2C.h>
#include "KVHC100.h"
#include <PCF8574.h>

#define MOT1_1 10
#define MOT1_2 9
#define MOT1_EN 11
#define MOT2_1 6
#define MOT2_2 5
#define MOT2_EN 12
#define MOT_FREQ 3000

#define EM_STOP A4

#define KVH_PHASE_OFFSET 0

#define PCF_ADDRESS 0x27
#define SONAREXTENDER_INT P7
#define BARRELHOLDER P6

extern Motor motorLeft, motorRight;

extern KVHC100 kvhc100;

extern SonarExtenderI2C sonar;

extern PCF8574 pcf;

/***
 * Inits JECCbot hardware
 */
void HWInit();

/***
 * Changes motor pwm base frequency.
 * Takes values from 0 to 16000 Hz.
 */
void changeMotorPwmFrequency(int pwmFrequency);

/***
 * Sets motors speeds without control ( PWM dutycycle only ).
 * Takes values from -100% to 100% for each motor.
 */
void setMotors(int speedLeft, int speedRight);

/***
 * Returns heading of robot to north ( -180 deg to 180 deg ).
 */
int getHeading();

int isEmergencyStop();

int isBarrel();

int getSonar(uint8_t number);

#endif
