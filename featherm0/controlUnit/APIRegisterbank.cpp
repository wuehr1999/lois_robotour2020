#include "APIRegisterbank.h"

APIRegister apiRegister;

void apiInit()
{
  for(int i = 0; i < REG_ADDRESS_RANGE; i++)
  {
    apiRegister.bench[i] = 0;
  }

  apiRegister.bench[REG_MOTOR_LEFT] = 0;
  apiRegister.bench[REG_MOTOR_RIGHT] = 0;
  apiRegister.bench[REG_STATE] = STATE_JOYDRIVE;

  apiRegister.availableAccesses[REG_VERSION] = REG_READ_ACCESS;
  apiRegister.availableAccesses[REG_MOTOR_LEFT] = REG_READ_WRITE_ACCESS;
  apiRegister.availableAccesses[REG_EMERGENCY_STOP] = REG_READ_ACCESS;
  apiRegister.availableAccesses[REG_MOTOR_RIGHT] = REG_READ_WRITE_ACCESS;
  apiRegister.availableAccesses[REG_BNO_HEADING] = REG_READ_ACCESS;
}
