#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

/***
 * Struct containing motor parameters
 */
typedef struct Motor
{
  byte pinPwm1, pinPwm2, pinInhibit;
  int pwmFrequency;
  int pwm1Dutycycle, pwm2Dutycycle;
  
  int interruptBaseFrequency, interruptCycles, interruptCyclecounter;
  
}Motor;

/***
 * Inits motor with corresponding pins, pwm frequency in Hz and motor update interrupt base frequency in kHz ( usually 16000 Hz )
 */
void motorInit(Motor *motor, byte pinPwm1, byte pinPwm2, byte pinInhibit, int pwmFrequency, int interruptBaseFrequency);

/***
 * Changes motor pwm frequency.
 * Takes frequency values from 0 to 16000 Hz.
 */
void motorChangePwmFrequency(Motor *motor, int pwmFrequency);

/***
 * Enables or disables motor according to enable state.
 */
void motorEnable(Motor *motor, int enableState);

/***
 * Sets motors speeds without control ( PWM dutycycle only ).
 * Takes values from -100% to 100%.
 */
void motorSetSpeed(Motor *motor, int speed);

/***
 * Breaks motor by setting both H-Bridge inputs High
 */
void motorBreak(Motor *motor);


/***
 * Updates motor, has to be called in interrupt handler with motor base frequency.
 */
void motorUpdate(Motor *motor);

#endif
