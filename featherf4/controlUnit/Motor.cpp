#include "Motor.h"

void motorInit(Motor *motor, byte pinPwm1, byte pinPwm2, byte pinInhibit, int pwmFrequency, int interruptBaseFrequency)
{
  motor->pinPwm1 = pinPwm1;
  motor->pinPwm2 = pinPwm2;
  motor->pinInhibit = pinInhibit;
  motor->pwmFrequency = pwmFrequency;
  motor->interruptBaseFrequency = interruptBaseFrequency;
  motor->interruptCycles = 2 * (interruptBaseFrequency / pwmFrequency);

  motor->pwm1Dutycycle = 0;
  motor->pwm2Dutycycle = 0;
  motor->interruptCyclecounter = 0;

  pinMode(pinPwm1, OUTPUT);
  pinMode(pinPwm2, OUTPUT);
  pinMode(pinInhibit, OUTPUT);

  digitalWrite(pinPwm1, LOW);
  digitalWrite(pinPwm2, LOW);
  digitalWrite(pinInhibit, LOW);
}

void motorChangePwmFrequency(Motor *motor, int pwmFrequency)
{
    if(pwmFrequency > motor->interruptBaseFrequency)
    {
      pwmFrequency = motor->interruptBaseFrequency;  
    }
    else if(pwmFrequency < 1)
    {
      pwmFrequency = 1;
    }
    
    motor->pwmFrequency = pwmFrequency;
    motor->interruptCycles = 2 * (motor->interruptBaseFrequency / pwmFrequency);
    motor->pwm1Dutycycle = 0;
}

void motorEnable(Motor *motor, int enableState)
{
  if(enableState)
  {
    digitalWrite(motor->pinInhibit, HIGH);
  }
  else
  {
    digitalWrite(motor->pinInhibit, HIGH);
  }
}

void motorSetSpeed(Motor *motor, int speed)
{
  if(speed < -100)
  {
    speed = -100;
  }
  else if(speed > 100)
  {
    speed = 100;
  }
  if(speed >= 0)
  {
    motor->pwm1Dutycycle = speed;
    motor->pwm2Dutycycle = 0;
  }
  else
  {
    speed = -speed;
    motor->pwm1Dutycycle = 0;
    motor->pwm2Dutycycle = speed;
  }
}

void motorBreak(Motor *motor)
{
  motor->pwm1Dutycycle = 100;
  motor->pwm2Dutycycle = 100;
}


void motorUpdate(Motor *motor)
{
  if(motor->interruptCycles >= motor->interruptCyclecounter)
  {
    if((motor->interruptCycles * motor->pwm1Dutycycle) / 100 >= motor->interruptCyclecounter)
    {
      digitalWrite(motor->pinPwm1, LOW);
    }
    else
    {
      digitalWrite(motor->pinPwm1, HIGH);
    }
    
    if((motor->interruptCycles * motor->pwm2Dutycycle) / 100 >= motor->interruptCyclecounter)
    {
      digitalWrite(motor->pinPwm2, LOW);
    }
    else
    {
      digitalWrite(motor->pinPwm2, HIGH);
    }

    motor->interruptCyclecounter ++;
  }
  else
  {
    motor->interruptCyclecounter = 0;
  }
}
