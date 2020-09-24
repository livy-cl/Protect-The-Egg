LaserPin = 2

setup()
{
  PinMode(LaserPin, OUTPUT)
}


loop()
{
  digitalWrite(LaserPin, HIGH);

  delay(1000)
}
