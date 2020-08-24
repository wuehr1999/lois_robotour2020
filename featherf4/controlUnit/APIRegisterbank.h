#ifndef API_REGISTER_BANK_H
#define API_REGISTER_BANK_H

#include <Arduino.h>
#include "APIStates.h"
#include "APIRegisterMapping.h"

#define REG_ADDRESS_RANGE 0xff

#define REG_READ_ACCESS 0x02
#define REG_WRITE_ACCESS 0x04
#define REG_READ_WRITE_ACCESS 0x06

typedef struct APIRegister
{
  short bench[REG_ADDRESS_RANGE];
  uint8_t availableAccesses[REG_ADDRESS_RANGE];
}APIRegister;

extern APIRegister apiRegister;

void apiInit();

#endif
