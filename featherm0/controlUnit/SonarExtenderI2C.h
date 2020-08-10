#ifndef SONAREXTENDERI2C_H
#define SONAREXTENDERI2C_H

#include <Arduino.h>

#include "TCA9535.h"

#define SONAREXTENDERI2C_TOCM(X) 100*X/2/30

class SonarExtenderI2C
{
  public:
  
  SonarExtenderI2C();

  void begin();
  
  uint8_t getMeasurementRaw(uint8_t sensorNumber);
  uint8_t getMeasurementCm(uint8_t sensorNumber);

  void read();
  void read(uint8_t sensorNumber);

  void startAutoread();
  void pauseAutoread();
  void stopAutoread();

  void autoreadCallback();
  
  private:

  TCA9535 tca;

  uint8_t interruptPin;

  uint8_t measurement0, measurement1, measurement2, measurement3;

  void trigger(uint8_t sensorNumber);
  void waitForEcho(uint8_t sensorNumber);
  uint8_t decode(uint8_t sensorNumber);
};

#endif
