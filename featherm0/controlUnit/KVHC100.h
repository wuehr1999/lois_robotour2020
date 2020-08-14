#ifndef KVHC100_H
#define KVHC100_H

#include <Arduino.h>

#define KVHC100_D 0.1

typedef struct KVHC100
{
  int phaseOffset;
  int heading;
} KVHC100;


void kvhc100Init(KVHC100 *kvh, int phaseOffset);

void kvhc100Update(KVHC100 *kvh);


#endif
