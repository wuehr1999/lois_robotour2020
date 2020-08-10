  #include "TCA9535.h"
  
  TCA9535::TCA9535()
  {
    address=TCA9535_DEFAULTADDRESS;
  }

  void TCA9535::begin(uint8_t address)
  {
    this->address = address;
    begin();
  }
  
  void TCA9535::begin()
  {
    Wire.begin();
  }

  void TCA9535::write(uint8_t registerNumber, uint8_t value)
  {
    Wire.beginTransmission(address);
    Wire.write(registerNumber);
    Wire.write(value);
    Wire.endTransmission();
  }
  
  
  uint8_t TCA9535::read(uint8_t registerNumber)
  {
    Wire.beginTransmission(address);
    Wire.write(registerNumber);
    Wire.endTransmission();
    
    Wire.requestFrom(address, (uint8_t)1);
    uint8_t value = Wire.read();
    Wire.endTransmission();
    
    return value;
  }
