  #include "SonarExtenderI2C.h"
  
  SonarExtenderI2C::SonarExtenderI2C()
  {
    measurement0 = 0;
    measurement1 = 0;
    measurement2 = 0;
    measurement3 = 0;
  
    interruptPin = -1; 

  }

  void SonarExtenderI2C::begin()
  {
    tca.begin();
    tca.write(TCA9535_REGISTER_CONFIG0, 0b00001000);
    tca.write(TCA9535_REGISTER_CONFIG1, 0b11111111);
    tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000111);
  }

  uint8_t SonarExtenderI2C::getMeasurementRaw(uint8_t sensorNumber)
  {
    uint8_t measurement;
    
    switch(sensorNumber)
    {
      case 0: measurement = measurement0; break;
      case 1: measurement = measurement1; break;
      case 2: measurement = measurement2; break;
      case 3: measurement = measurement3; break;
      default: measurement = -1; break;
    }

    return measurement;
  }
  
  uint8_t SonarExtenderI2C::getMeasurementCm(uint8_t sensorNumber)
  {
    uint8_t measurement;
    
    switch(sensorNumber)
    {
      case 0: measurement = measurement0; break;
      case 1: measurement = measurement1; break;
      case 2: measurement = measurement2; break;
      case 3: measurement = measurement3; break;
      default: measurement = -1; break;
    }

    if(measurement > -1)
    {
      measurement = SONAREXTENDERI2C_TOCM(measurement);
    }

    return measurement;
  }

  void SonarExtenderI2C::read()
  {
    for(uint8_t i = 0; i <= 3; i++)
    {
      read(i);
    }
  }
  
  void SonarExtenderI2C::read(uint8_t sensorNumber)
  {
    trigger(sensorNumber);
    waitForEcho(sensorNumber);
    decode(sensorNumber);
  }

  void SonarExtenderI2C::startAutoread()
  {
    tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000100);
  }

  void SonarExtenderI2C::pauseAutoread()
  {
      tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000101);  
  }
  
  void SonarExtenderI2C::stopAutoread()
  {
    tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000111);
  }

void SonarExtenderI2C::autoreadCallback()
{
   for(int i = 0; i <= 3; i++)
   {
     decode(i);
   }
   startAutoread();
}

  void SonarExtenderI2C::trigger(uint8_t sensorNumber)
  {
    tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000000);
    
    uint8_t data;

    switch(sensorNumber)
    {
      case 0: data = 0b00010000; break;
      case 1: data = 0b00100000; break;
      case 2: data = 0b01000000; break;
      case 3: data = 0b10000000; break;
      default: data = 0b00000000; break;
    }

    tca.write(TCA9535_REGISTER_OUTPUT0, data);

    delay(100);
    tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000111);
  }
  
  void SonarExtenderI2C::waitForEcho(uint8_t sensorNumber)
  {
    for(int i = 0; i < 100; i++)
    {
      if(tca.read(TCA9535_REGISTER_INPUT0)<8)
      {
        break;
      }
      delay(1);
    }
  }
  
  uint8_t SonarExtenderI2C::decode(uint8_t sensorNumber)
  {
    tca.write(TCA9535_REGISTER_OUTPUT0, sensorNumber);

    uint8_t measurement = tca.read(TCA9535_REGISTER_INPUT1);
    tca.write(TCA9535_REGISTER_OUTPUT0, 0b00000111);

    switch(sensorNumber)
    {
      case 0: measurement0 = measurement; break;
      case 1: measurement1 = measurement; break;
      case 2: measurement2 = measurement; break;
      case 3: measurement3 = measurement; break;
    }
  }
  
