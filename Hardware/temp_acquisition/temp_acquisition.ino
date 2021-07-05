// Includes
#include <TimeLib.h>


// Variables 
int analogTemp_pin = A1;          // ADC pin connected to variable output of the temp. sensor
int analogPWM_pin = 6;            // PWM output pin used to drive fan commutator/speed
int digitalRelayHI_pin = 13;      // Discrete used to toggle relay HI line on or off
int digitalRelayLO_pin = 12;      // Discrete used to toggle relay LO line on or off
float excitation_voltage = 4.5;   // Excitation voltage across temp. sensor
float offset = 0.5;               // Offset value from tmp36 datasheet
float sensor_factor = 1024.0;     // Analog voltage range is linearly proportional from 0 to 1023 with 0=0v, 1023=excitation voltage - map raw value to voltage range.
float map_percent = 100.0;        // Percentage range
float c_factor = (9.0/5.0);       // Factor used to convert Celsius to Fahrenheit
float f_constant = 32.0;          // Constant factor added to Celsius to Fahrenheit conversion.
const int data_columns = 2;       // Number of types of data
const int data_rows = 6;          // Total number of data points taken per type of data.
const float max_temp = 80;        // Maximum temperature that will represent 100% duty cycle to drive fan
const float min_temp = 74;        // Minimum temperature that will represent 0% duty cycle to drive fan
const float temp_range = max_temp-min_temp;
const int pwm_max_bits = 255;     // 255=100% : 0=0% duty cycle for Arduino analogWrite() API call

// Main buffer used to store values and datetime over a sampling interval.
//char values_overTime[data_rows][data_columns] = {{'null', 'null', 'null', 'null', 'null', 'null'} , {'null', 'null', 'null', 'null', 'null', 'null'}};
//char values_overTime[data_rows][data_columns];


// Initialization function
void setup() {
  // Initialize serial port for testing/debugging
  Serial.begin(9600);  // Initialize the serial port with specific baud rate
  pinMode(analogPWM_pin, OUTPUT);  // Setup analog pin to "output" mode in order to drive pwm signals
  pinMode(digitalRelayHI_pin, OUTPUT);  // Setup discrete line to "output" mode to drive HI/LO states
  pinMode(digitalRelayLO_pin, OUTPUT);  // Setup discrete line to "output" mode to drive HI/LO states
}

// Main loop to perform operations and grab data from sensor(s)
void loop() {
  int shifter = 0;
  while(true) {
    float values[data_rows]; // Buffer used to store values
    for (int i = 0; i < data_rows; i++) {
      int raw_bitValue = analogRead(analogTemp_pin);                // Read raw bit values from ADC
      float miliVoltage_range = raw_bitValue * excitation_voltage;  // Convert raw bit values to excitation voltage percentage
      float miliVoltage = miliVoltage_range / sensor_factor;        // Map excitation percentage to degree/voltage range of temp. sensor
      float Celsius = (miliVoltage - offset) * map_percent;         // Map milivoltage to Celsius
      float Fahrenheit = (Celsius * c_factor) + f_constant;         // Convert Celsius to Fahrenheit
  
      // Post output to serial port for debugging
      Serial.println("Temperature Reading (°Fahrenheit) : " + String(Fahrenheit));
      values[i] = Fahrenheit;
      Serial.println("Value_" + String(i) + ": " + String(values[i]));
      
//      // Grab data, time and store values in FIFO array
//      int h = hour();
//      int mi = minute();
//      int s = second();
//      int mo = month();
//      int d = day();
//      int y = year();
//      String datetime = String(h) + "-" + String(mi) + "-" + String(s) + "  " + String(mo) + "/" + String(d) + "/" + String(y);
//      //char datetime[sizeof(String(datetime_str))] = {datetime_str};
//      Serial.println("datetime: " + datetime);
////      Serial.println("hour = " + String(h));
////      Serial.println("minute = " + String(m));
////      Serial.println("second = " + String(s));
//      // Store datetime and value
//      shifter++; // Increment the shifter once the data buffer is full
//      if (shifter >= data_rows){
//        // shifter = 0;  // Reset FIFO array element assignment if we reach the max size
//        for (int j = 0; j < data_columns; j++){
//          for (int k = 1; k < data_rows; k++){
//            values_overTime[(data_rows - k)-1][j] = values_overTime[data_rows - k][j];  // Shift all values over to next element
//          }
//        }
//        // Once buffer is filled up, only write to first value in each column.
//        // char Fahrenheit_String[sizeof(String(Fahrenheit))] = {Fahrenheit};
//        // Fahrenheit_String.toChar(values_overTime[0][0], sizeof(Fahrenheit_String));
//        // datetime.toChar(values_overTime[0][1], sizeof(datetime));
//        values_overTime[0][0] = Fahrenheit;
//        values_overTime[0][1] = datetime;
//      else{  // Fill up buffer initially
//        // char Fahrenheit_String[sizeof(String(Fahrenheit))] = {Fahrenheit};
//        values_overTime[i][0] = Fahrenheit;
//        values_overTime[i][1] = datetime;
//        //values_overTime[i][0] = String(Fahrenheit);
//        // Fahrenheit_String.toChar(values_overTime[i][0], sizeof(Fahrenheit_String));
//        // datetime.toChar(values_overTime[i][1], sizeof(datetime));
//      }
//      Serial.println("buffer: " + String(values_overTime));
//    // If the temp from sensor is between our range of interest, set fan pwm accordingly  
      if ((Fahrenheit < max_temp) && (Fahrenheit > min_temp)){  
        digitalWrite(digitalRelayHI_pin, HIGH);                 // Turn relay HI line ON - allows power to fan.
        digitalWrite(digitalRelayLO_pin, HIGH);                 // Turn relay LO line ON
        float pwm_percent = (Fahrenheit - min_temp)/temp_range; // Map pwm percentage relative to °F range
        int pwm_bit_range = (int)(pwm_max_bits*pwm_percent);    // Set bit range for pwm - round to nearest integer
        analogWrite(analogPWM_pin, pwm_bit_range);              // Sets the pwm duty cycle - frequency is roughly ~490hz.
      }
      else{
        if (Fahrenheit > max_temp){  // If temp is higher than max_temp, drive fan at 100%
          digitalWrite(digitalRelayHI_pin, HIGH);               // Turn relay HI line ON - allows power to fan.
          digitalWrite(digitalRelayLO_pin, HIGH);               // Turn relay LO line ON
          analogWrite(analogPWM_pin, pwm_max_bits);             // Sets the pwm duty cycle to max %
        }
        else{  // If temp is lower than min_temp, turn fan off
          digitalWrite(digitalRelayHI_pin, LOW);                // Turn relay HI line OFF - turn power off to fan.
          digitalWrite(digitalRelayLO_pin, LOW);                // Turn relay LO line OFF
          analogWrite(analogPWM_pin, 0);                        // Sets the pwm duty cycle to 0%
        }
      }
      delay(1000); // Delay loop by milisecond(s) interval
      
      }
    }
    

    
}
