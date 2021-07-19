// Includes
#include <TimeLib.h>

// Variables 
int analogTemp_pin = A1;          // ADC pin connected to variable output of the temp. sensor
int analogPWM_pin = 5;            // PWM output pin used to drive fan commutator/speed
int counterRPM_pin = 3;           // Digital pin connected to tachometer of the fan.
int digitalRelayHI_pin = 6;       // Discrete used to toggle relay HI line on or off
int digitalRelayLO_pin = 7;       // Discrete used to toggle relay LO line on or off
float excitation_voltage = 4.5;   // Excitation voltage across temp. sensor
float temp_offset_fan_on = 12.0;  // When the fan is on, excitation voltage increases, changing the temp measurement.
bool  fan_on = false;             // Flag used to determine when fan is on or off
float offset = 0.5;               // Offset value from tmp36 datasheet
float sensor_factor = 1024.0;     // Analog voltage range is linearly proportional from 0 to 1023 with 0=0v, 1023=excitation voltage - map raw value to voltage range.
float map_percent = 100.0;        // Percentage range
float c_factor = (9.0/5.0);       // Factor used to convert Celsius to Fahrenheit
float f_constant = 32.0;          // Constant factor added to Celsius to Fahrenheit conversion.
const int data_columns = 2;       // Number of types of data
const int data_rows = 6;          // Total number of data points taken per type of data.
float max_temp = 80;              // Maximum temperature that will represent 100% duty cycle to drive fan
float min_temp = 76;              // Minimum temperature that will represent 0% duty cycle to drive fan
float temp_range;                 // Variable used to calculate the range in which pwm duty cycle % will be mappped to.
const int pwm_max_bits = 255;     // 255=100% : 0=0% duty cycle for Arduino analogWrite() API call
int   count_risingEdges = 0;      // Counter used to keep up with rising edge ticks for rpm calculation.
float   rpm;                      // Variable used to convert electrical pulses to revolutions per minute for the fan.


// Initialization function
void setup() {
  // Initialize serial port for testing/debugging
  Serial.begin(115200);  // Initialize the serial port with specific baud rate
  pinMode(analogPWM_pin, OUTPUT);                                 // Setup analog pin to "output" mode in order to drive pwm signals
  pinMode(counterRPM_pin, INPUT);                                 // Setup RPM analog input line
  pinMode(digitalRelayHI_pin, OUTPUT);                            // Setup discrete line to "output" mode to drive HI/LO states
  pinMode(digitalRelayLO_pin, OUTPUT);                            // Setup discrete line to "output" mode to drive HI/LO states
  attachInterrupt(digitalPinToInterrupt(counterRPM_pin), get_rpm, RISING);// Register a callback function for when a global interrupt is triggered.
}

// Callback function that will increment to count every tick from rising edge - this will calculate the rpm.
void get_rpm(){
  count_risingEdges++;
}

// Main loop to perform operations and grab data from sensor(s)
void loop() {
  // Embedded loop that will run indefinitely  
  while(true) {
    temp_range = max_temp-min_temp;                               // Grab range for pwm % duty cycle to be mapped to temperature.
    int raw_bitValue = analogRead(analogTemp_pin);                // Read raw bit values from ADC
    float miliVoltage_range = raw_bitValue * excitation_voltage;  // Convert raw bit values to excitation voltage percentage
    float miliVoltage = miliVoltage_range / sensor_factor;        // Map excitation percentage to degree/voltage range of temp. sensor
    float Celsius = (miliVoltage - offset) * map_percent;         // Map milivoltage to Celsius
    float Fahrenheit = (Celsius * c_factor) + f_constant;         // Convert Celsius to Fahrenheit

    // if the fan is ON, account for increase in excitation voltage used in temperature calculation.
    if (fan_on){ 
      Fahrenheit = Fahrenheit - temp_offset_fan_on;
    }

     // Save output to write to serial port 
    float tempValue = Fahrenheit;                                 // Buffer used to store values
    
    // If the temp from sensor is between our range of interest, set fan pwm accordingly  
    if ((Fahrenheit < max_temp) && (Fahrenheit > min_temp)){  
      fan_on = true;                                              // Indicate that the fan is on.
      digitalWrite(digitalRelayHI_pin, LOW);                      // Turn relay HI line ON - allows power to fan.
      digitalWrite(digitalRelayLO_pin, LOW);                      // Turn relay LO line ON
      float pwm_percent = (Fahrenheit - min_temp)/temp_range;     // Map pwm percentage relative to °F range
      int pwm_bit_range = (int)(pwm_max_bits*pwm_percent);        // Set bit range for pwm - round to nearest integer
      analogWrite(analogPWM_pin, pwm_bit_range);                  // Sets the pwm duty cycle - frequency is roughly ~490hz.
    }
    else{
      if (Fahrenheit > max_temp){  // If temp is higher than max_temp, drive fan at 100% - - polarity is inverse
        fan_on = true;                                            // Indicate that the fan is ON
        digitalWrite(digitalRelayHI_pin, LOW);                    // Turn relay HI line ON - allows power to fan.
        digitalWrite(digitalRelayLO_pin, LOW);                    // Turn relay LO line ON
        analogWrite(analogPWM_pin, pwm_max_bits);                 // Sets the pwm duty cycle to max %
      }
      else{  // If temp is lower than min_temp, turn fan off - polarity is inverse
        fan_on = false;                                           // Indicate that the fan is off
        digitalWrite(digitalRelayHI_pin, HIGH);                   // Turn relay HI line OFF - turn power off to fan.
        digitalWrite(digitalRelayLO_pin, HIGH);                   // Turn relay LO line OFF
        analogWrite(analogPWM_pin, 0);                            // Sets the pwm duty cycle to 0%
      }
    }
    
    count_risingEdges = 0;                                        // Reset counter for rpm calculation.
    sei();                                                        // Trigger the global interrupts
    delay(1000);                                                  // Delay loop by milisecond(s) interval to determine rpm.
    cli();                                                        // End the global interrupts
    rpm = count_risingEdges/2.0;                                  // Each rising edge represents half of a rotation.

    // Write data to serial port for database thread to record
    Serial.println(tempValue);
    Serial.println(rpm);
  }
}
