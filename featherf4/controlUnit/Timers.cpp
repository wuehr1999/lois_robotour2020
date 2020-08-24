#include "Timers.h"

void start1000Hz()
{
  TIM_TypeDef *instance1000 = TIM1;
  HardwareTimer *timer1000 = new HardwareTimer(instance1000);
  timer1000->setOverflow(1000, HERTZ_FORMAT);
  timer1000->attachInterrupt(interrupt1000Hz);
  timer1000->resume();
}


void start16000Hz()
{
  TIM_TypeDef *instance16000 = TIM2;
  HardwareTimer *timer16000 = new HardwareTimer(instance16000);
  timer16000->setOverflow(16000, HERTZ_FORMAT);
  timer16000->attachInterrupt(interrupt16000Hz);
  timer16000->resume();
}
