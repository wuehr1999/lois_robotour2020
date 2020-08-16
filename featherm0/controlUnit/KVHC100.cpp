#include "KVHC100.h"

KVHC100 kvhdefault;

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
  memcpy(kvh, &kvhdefault, sizeof(KVHC100));
}

void SERCOM0_Handler()
{
  Serial1.IrqHandler();

  static String kvhString = "";
  static bool startFound = false;
  
  char c = Serial1.read();

  if(c == '$')
  {
    kvhString = c;
    startFound = true;
  }
  else if(c == '\n')
  {
    if(startFound)
    {
      String headingStr = kvhString.substring(7, 10);
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
    
      int lastheading = kvhdefault.heading;
      if(lastheading < 0)
      {
        lastheading = -lastheading;
      }
    
      int p = 1;
      if(heading < 0)
      {
        p = -p;
        heading = -heading;
      }
      
      //kvhdefault.heading= p * heading + (int)(KVHC100_D * (float)(heading - lastheading));  
      kvhdefault.heading = p * (float)(lastheading + KVHC100_D *heading) / (float)(1 + KVHC100_D);
    }
    startFound = false;
  }
  else
  {
    kvhString += c;
  }
}
