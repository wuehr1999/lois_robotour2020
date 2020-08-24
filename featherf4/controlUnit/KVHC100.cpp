#include "KVHC100.h"

KVHC100 kvhdefault;

void kvhc100Init(KVHC100 *kvh, int phaseOffset)
{
  kvh->phaseOffset = phaseOffset;

  Serial3.begin(4800);

  String kvhInitStr = "s\r";
  String kvhConfigNmeaStr = "=t,0\r";
  String kvhConfigSpeedStr = "=r,600\r";
  String kvhConfigUnitStr = "=i,d\r";
  Serial3.print(kvhInitStr);
  delay(100);
  Serial3.print(kvhConfigNmeaStr);
  delay(100);
  Serial3.print(kvhConfigSpeedStr);
  delay(100);
  Serial3.print(kvhConfigUnitStr);
}

void kvhc100Update(KVHC100 *kvh)
{
  memcpy(kvh, &kvhdefault, sizeof(KVHC100));
}

void serialEvent3()
{
  static String kvhString = "";
  static bool startFound = false;
  static int counter = -1;

  //while(Serial3.available()){
  if(Serial3.available())
  {
    char c = Serial3.read();
    counter ++;
  
    if(c == '$')
    {
      counter = -1;
      kvhString = c;
      startFound = true;
    }
    else if(c == '\n' || counter == 10)
    {
      counter = 0;
      
      if(startFound && kvhString.length() > 10)
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
        
        kvhdefault.heading= p * heading + (int)(KVHC100_D * (float)(heading - lastheading));  
        //kvhdefault.heading = p * (float)(lastheading + KVHC100_D *heading) / (float)(1 + KVHC100_D);
      }
      startFound = false;
      Serial3.flush();
    }
    else
    {
      kvhString += c;
    }
  }
}
