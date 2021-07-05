// Variables 
int analog_pin = A1;  // ADC pin connected to variable output of the temp. sensor
float excitation_voltage = 5.0;  // Excitation voltage across temp. sensor
float offset = 0.5; // Offset value from tmp36 datasheet
float sensor_factor = 1024.0;  // Analog voltage range is linearly proportional from 0 to 1023 with 0=0v, 1023=excitation voltage - map raw value to voltage range.
float map_percent = 100.0;  // Percentage range
float c_factor = (9.0/5.0);
float f_constant = 32.0;

// Initialization function
void setup() {
  // Initialize serial port for testing/debugging
  Serial.begin(9600);
}

// Main loop to perform operations and grab data from sensor(s)
void loop() {
  while(true) {

    int raw_bitValue = analogRead(analog_pin);  // Read raw bit values from ADC
    float miliVoltage_range = raw_bitValue * excitation_voltage;  // Convert raw bit values to excitation voltage percentage
    float miliVoltage = miliVoltage_range / sensor_factor;  // Map excitation percentage to degree/voltage range of temp. sensor
    float Celsius = (miliVoltage - offset) * map_percent;  // Map milivoltage to Celsius
    float Fahrenheit = (Celsius * c_factor) + f_constant; // Convert Celsius to Fahrenheit

    // Post output to serial port for debugging
    Serial.println("Temperature Reading (°Fahrenheit) : " + String(Fahrenheit));
    delay(1000); // Delay loop by milisecond(s) interval
  }
}
