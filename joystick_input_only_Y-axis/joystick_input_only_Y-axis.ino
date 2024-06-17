const int yPin = A1;  // Y-axis connected to analog pin A1

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 baud rate
}

void loop() {
  int yValue = analogRead(yPin);  // Read the Y-axis value from the joystick
  Serial.println(yValue);  // Send the Y-axis value over serial
  delay(50);  // Delay to control the rate of serial communication
}
