#include "MoveUtils.h"

void moveHeading()
{
  static int esum = 0;
  
  int speedMax =  apiRegister.bench[REG_AVG_SPEED];
  int heading = apiRegister.bench[REG_DEST_HEADING];
  int compassHeading = apiRegister.bench[REG_COMPASS_HEADING];
  int error = heading - compassHeading;

  if(error > 180)
  {
    error = error - 360;
  }
  else if(error < -180)
  {
    error = error + 360;
  }

  esum += error;

  if((heading - MOVE_TOLHEADING) <= compassHeading && compassHeading <= (heading + MOVE_TOLHEADING))
  {
    esum = 0;
  }
  int deltaSpeed = (int)(error * MOVE_PHEADING) + (int)(esum * MOVE_IHEADING);

  int left = speedMax + deltaSpeed;
  int right = speedMax - deltaSpeed;

  if(left < 0)
  {
   left = 0;
  }
  else if(left > speedMax)
  {
    left = speedMax;
  }

  if(right < 0)
  {
   right = 0;
  }
  else if(right > speedMax)
  {
   right = speedMax;
  }
  setMotors(left, right);
}
