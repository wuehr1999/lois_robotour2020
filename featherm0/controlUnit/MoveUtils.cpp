#include "MoveUtils.h"

void moveHeading(int heading, int speedMax)
{
  int error = heading - getHeading();

  if(error > 180)
  {
    error = error - 360;
  }
  else if(error < -180)
  {
    error = error + 360;
  }

  int deltaSpeed = (int)(error * MOVE_PHEADING);

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
