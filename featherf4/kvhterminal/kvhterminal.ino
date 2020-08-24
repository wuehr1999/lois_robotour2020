void setup() {
  Serial.begin(115200);
  Serial3.begin(4800);
}

void loop() {
   /* // read from port 0, send to port 1:
    if (Serial.available()) {
    char inByte = Serial.read();
    Serial1.print(inByte);
    }
    // read from port 1, send to port 0:
  if (Serial1.available()) {
    char inByte = Serial1.read();
    Serial.print(inByte);
  }*/
}

void serialEvent3()
{
      // read from port 1, send to port 0:
  if (Serial3.available()) {
    char inByte = Serial3.read();
    Serial.print(inByte);
  }
}

void serialEvent()
{
      // read from port 0, send to port 1:
    if (Serial.available()) {
    char inByte = Serial.read();
    Serial3.print(inByte);
    }
}
