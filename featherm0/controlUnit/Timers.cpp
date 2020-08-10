#include "Timers.h"

void start1000Hz()
{
  GCLK->CLKCTRL.reg = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_ID(GCM_TC4_TC5)) ;
  while (GCLK->STATUS.bit.SYNCBUSY);
  TcCount16* TC = (TcCount16*) TC5;
  TC->CTRLA.reg = TC_CTRLA_SWRST;
  while (TC->STATUS.bit.SYNCBUSY);
  while (TC->CTRLA.bit.SWRST);
  TC->CTRLA.reg |= TC_CTRLA_MODE_COUNT16;
  while (TC->STATUS.bit.SYNCBUSY);
  TC->CTRLA.reg |= TC_CTRLA_WAVEGEN_MFRQ;
  while (TC->STATUS.bit.SYNCBUSY);  
  TC->CTRLA.reg |= TC_CTRLA_PRESCALER_DIV1 | TC_CTRLA_ENABLE; 
  while (TC->STATUS.bit.SYNCBUSY);
  TC->CC[0].reg = (uint16_t) (SystemCoreClock-1);
  while (TC->STATUS.bit.SYNCBUSY);
  NVIC_DisableIRQ(TC5_IRQn);
  NVIC_ClearPendingIRQ(TC5_IRQn);
  NVIC_SetPriority(TC5_IRQn, 0);
  NVIC_EnableIRQ(TC5_IRQn);
  TC->INTENSET.bit.MC0 = 1;
  while (TC->STATUS.bit.SYNCBUSY);
  TC->CTRLA.reg |= TC_CTRLA_ENABLE; 
  while (TC->STATUS.bit.SYNCBUSY);
}

void TC5_Handler()
{
  TcCount16* TC = (TcCount16*) TC5;
  if (TC->INTFLAG.bit.MC0 == 1) {
    TC->INTFLAG.bit.MC0 = 1;
    interrupt1000Hz();
  }  
}

void start16000Hz()
{
  REG_GCLK_CLKCTRL = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_ID_TCC2_TC3) ;
  while (GCLK->STATUS.bit.SYNCBUSY);  
  TcCount16* TC = (TcCount16*) TC3;
  TC->CTRLA.reg |= TC_CTRLA_MODE_COUNT16;
  while (TC->STATUS.bit.SYNCBUSY);  
  TC->CTRLA.reg |= TC_CTRLA_WAVEGEN_MFRQ;
  while (TC->STATUS.bit.SYNCBUSY);
  TC->CTRLA.reg |= TC_CTRLA_PRESCALER_DIV1;
  while (TC->STATUS.bit.SYNCBUSY);
  int compareValue = 1535;
  TC->COUNT.reg = map(TC->COUNT.reg, 0, TC->CC[0].reg, 0, compareValue);
  TC->CC[0].reg = compareValue;
  while (TC->STATUS.bit.SYNCBUSY);
  TC->INTENSET.reg = 0;
  TC->INTENSET.bit.MC0 = 1;
  NVIC_EnableIRQ(TC3_IRQn);
  TC->CTRLA.reg |= TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY);
}

void TC3_Handler()
{
  TcCount16* TC = (TcCount16*) TC3;
  if (TC->INTFLAG.bit.MC0 == 1) {
    TC->INTFLAG.bit.MC0 = 1;
    interrupt16000Hz();
  }
}
