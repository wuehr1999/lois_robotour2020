#include "JECCbotAPI.h"

void initJECCbot()
{
  apiInit();
  HWInit();
}

void generateResponse(char *resp, uint16_t address);
void generateResponse(char *resp, char *errorMessage);

void runApiStatemachine();

APIResponse processCommand(char* command)
{
  uint8_t len = strlen(command) + 1;
  
  char cmd[len];
  strcpy(cmd, command);

  APIResponse response;

  response.error = -1;

  if(cmd[0] == PROTOCOLL_STARTFLAG && cmd[len-2] == PROTOCOLL_STOPFLAG)
  {
    char accessModeStr[2];
    char addressStr[4]; 
    uint8_t accessMode;
    uint16_t address;
    uint16_t value;

    strncpy(accessModeStr, &cmd[1], 2);
    strncpy(addressStr, &cmd[3], 4);
    accessMode = atoi(accessModeStr);
    address = (uint16_t)strtol(addressStr, NULL, 16);

    if(REG_READ_ACCESS == accessMode && address < REG_ADDRESS_RANGE && !(REG_WRITE_ACCESS == apiRegister.availableAccesses[address]))
    {
      generateResponse(response.message, address);
    }
    else if(REG_WRITE_ACCESS == accessMode && address < REG_ADDRESS_RANGE && !(REG_READ_ACCESS == apiRegister.availableAccesses[address]) && address < REG_ADDRESS_RANGE && len>9)
    {
      char valueStr[len - 9];    
      strncpy(valueStr, &cmd[7], (len - 9)); 
      value = (short)strtol(valueStr, NULL, 16);
      apiRegister.bench[address] = value;
      generateResponse(response.message, address);
    }
    else
    {
      generateResponse(response.message, PROTOCOLL_ERROR_ACCESS);
    }
  }
  else
  {
    generateResponse(response.message, PROTOCOLL_ERROR_FORMAT);
  }
  return response;
}

void updateJECCbot()
{
  apiRegister.bench[REG_BNO_HEADING] = getHeading();
  runApiStatemachine();
}

void generateResponse(char *resp, uint16_t address)
{
  sprintf(resp, "%c%04x%04x%c", PROTOCOLL_STARTFLAG, address, (unsigned short)apiRegister.bench[address], PROTOCOLL_STOPFLAG);
}

void generateResponse(char *resp, char *errorMessage)
{
  sprintf(resp, "%c%s%c", PROTOCOLL_STARTFLAG, errorMessage, PROTOCOLL_STOPFLAG);
}

void runApiStatemachine()
{
  if(apiRegister.bench[REG_STATE] == STATE_JOYDRIVE)
  {
    setMotors((int)apiRegister.bench[REG_MOTOR_LEFT], (int)apiRegister.bench[REG_MOTOR_RIGHT]);
  }
  else if(apiRegister.bench[REG_STATE] == STATE_HEADINGDRIVE)
  {
    moveHeading(apiRegister.bench[REG_BNO_HEADING], apiRegister.bench[REG_AVG_SPEED]);
  }
}
