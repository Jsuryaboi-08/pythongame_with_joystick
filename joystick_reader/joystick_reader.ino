int joystickPin = A1; 

void setup() {
  Serial.begin(115200);
}

void loop() {
  int y_value = analogRead(joystickPin);
  y_value = map(y_value, 0, 700, 0, 480); // Map the joystick value to the screen height
  Serial.println(y_value);
  delay(10);
}