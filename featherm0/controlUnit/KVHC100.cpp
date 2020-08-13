#include "KVHC100.h"

void kvhc100Init(KVHC100 *kvh, int phaseOffset)
{
  kvh->phaseOffset = phaseOffset;

  Serial1.begin(4800);

  String kvhInitStr = "s\r";
  String kvhConfigNmeaStr = "=t,0\r";
  String kvhConfigSpeedStr = "=r,600\r";
  String kvhConfigUnitStr = "=i,d\r";
  Serial1.print(kvhInitStr);
  delay(100);
  Serial1.print(kvhConfigNmeaStr);
  delay(100);
  Serial1.print(kvhConfigSpeedStr);
  delay(100);
  Serial1.print(kvhConfigUnitStr);
}

void kvhc100Update(KVHC100 *kvh)
{
  char c = ' ';
  while(c != '$')
  {
    if(Serial1.available())
    {
      c = Serial1.read();
    }
  }
  String rawData = "";
  rawData += c;
  while(c != '\n')
  {
    if(Serial1.available())
    {
      c = Serial1.read();
      rawData += c;
    }
  }
  //$HCHDT,296.2,T*26
  //Serial.print(rawData);
  String headingStr = rawData.substring(7, 10);
  //Serial.println(headingStr);
  int heading = headingStr.toInt();

    if(heading > 360)
  {
    heading = heading - 360;
  }
  
  if(heading>180)
  {
    heading=heading-360;
  }
  
  kvh->heading=heading;  
}
