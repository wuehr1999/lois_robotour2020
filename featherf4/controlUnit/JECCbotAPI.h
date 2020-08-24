#ifndef JECCBOT_API_H
#define JECCBOT_API_H

#include "APIStates.h"
#include "APIRegisterMapping.h"
#include "APIRegisterbank.h"
#include "HWDriver.h"
#include "MoveUtils.h"

#define PROTOCOLL_STARTFLAG  ':'
#define PROTOCOLL_STOPFLAG '\n'
#define PROTOCOLL_ERROR_FORMAT "e00000000"
#define PROTOCOLL_ERROR_ACCESS "e00000001"

typedef struct APIResponse
{
  char message[12];
  uint8_t error; 
}APIResponse;

extern bool locked;

void initJECCbot();

APIResponse processCommand(char* command);

void updateJECCbot();
#endif
