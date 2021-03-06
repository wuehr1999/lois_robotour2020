#include "JECCbotAPI.h"

bool locked;

void initJECCbot()
{
  locked = false;
  apiInit();
  HWInit();
}

void generateResponse(uint16_t address);
void generateResponse(char *errorMessage);

void runApiStatemachine();


APIResponse response;

APIResponse processCommand(char* command)
{
  char accessModeStr[4];
  char addressStr[6]; 
  uint8_t accessMode;
  uint16_t address;
  uint16_t value;
  char cmd[15];
  uint8_t len;
  char valueStr[6];  

  len = strlen(command) + 1;
  if(len > 0)
  {
    strncpy(cmd, command, len);
  }


  response.error = -1;

  if(len > 8 && cmd[0] == PROTOCOLL_STARTFLAG && cmd[len-2] == PROTOCOLL_STOPFLAG)
  {
    strncpy(accessModeStr, &cmd[1], 2);
    strncpy(addressStr, &cmd[3], 4);
    accessMode = atoi(accessModeStr);
    address = (uint16_t)strtol(addressStr, NULL, 16);

    if(REG_READ_ACCESS == accessMode && address < REG_ADDRESS_RANGE && !(REG_WRITE_ACCESS == apiRegister.availableAccesses[address]))
    {
      generateResponse(address);
    }
    else if(REG_WRITE_ACCESS == accessMode && address < REG_ADDRESS_RANGE && !(REG_READ_ACCESS == apiRegister.availableAccesses[address]))
    {  
      strncpy(valueStr, &cmd[7], (len - 9)); 
      value = (short)strtol(valueStr, NULL, 16);
      apiRegister.bench[address] = value;
      generateResponse(address);
    }
    else
    {
      generateResponse(PROTOCOLL_ERROR_ACCESS);
    }
  }
  else
  {
    generateResponse(PROTOCOLL_ERROR_FORMAT);
  }
  return response;
}

void updateJECCbot()
{
  apiRegister.bench[REG_COMPASS_HEADING] = getHeading();
  
  apiRegister.bench[REG_EMERGENCY_STOP] = isEmergencyStop();
  
  apiRegister.bench[REG_SONAR_LEFT] = getSonar(3);
  apiRegister.bench[REG_SONAR_MIDDLE] = getSonar(2);
  apiRegister.bench[REG_SONAR_RIGHT] = getSonar(1);

  apiRegister.bench[REG_BARREL] = isBarrel();
  runApiStatemachine();
}

void generateResponse(uint16_t address)
{
  sprintf(response.message, "%c%04x%04x%c", PROTOCOLL_STARTFLAG, address, (unsigned short)apiRegister.bench[address], PROTOCOLL_STOPFLAG);
}

void generateResponse(char *errorMessage)
{
  sprintf(response.message, "%c%s%c", PROTOCOLL_STARTFLAG, errorMessage, PROTOCOLL_STOPFLAG);
}

void runApiStatemachine()
{
  if(apiRegister.bench[REG_STATE] == STATE_JOYDRIVE)
  {
    setMotors((int)apiRegister.bench[REG_MOTOR_LEFT], (int)apiRegister.bench[REG_MOTOR_RIGHT]);
  }
  else if(apiRegister.bench[REG_STATE] == STATE_HEADINGDRIVE)
  {
    moveHeading();
  }
}
