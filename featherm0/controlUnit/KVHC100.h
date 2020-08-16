#ifndef KVHC100_H
#define KVHC100_H

#include <Arduino.h>

#define KVHC100_D 4


/***Struct for storing KVHC100 data***/
typedef struct KVHC100
{
  int phaseOffset;
  int heading;
} KVHC100;

/***Inits KVH with correct opmode***/
void kvhc100Init(KVHC100 *kvh, int phaseOffset);

/***Updates KVH Data struct***/
void kvhc100Update(KVHC100 *kvh);

#endif
