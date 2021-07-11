# This file is responsible for receiving data from the Arduino/MCU serial port.
import serial
import time
import datetime
import json
import threading


# Class used to read temp values from MCU over serial port
class TempSensor(object):
    def __init__(self):
        self.temp = 0;
        self.serial_port = 'COM3'       # Specific serial port connected to Arduino
        self.baud_rate = 9600           # Baud rate used on specific com port
        try:
            self.serialHandle = serial.Serial(self.serial_port, self.baud_rate)  # Initialize com port
        except Exception as e:
            print(e)
        self.dataset_rows = 6           # Number of data points in each column
        self.dataset_cols = 2           # Number of data groups
        self.serial_loop_freq = 1.5     # Frequency in which serial buffer is filled with bytes
        # TODO: Remove - only using for testing purposes
        self.current_thread = threading.currentThread().ident
        print(self.current_thread)

    def get_data_serial_port(self):  # Grab temperature value from serial port of Arduino
        final_str = None
        try:
            recv_bits = self.serialHandle.readline()
            bits_toStr = recv_bits.decode()  # Convert raw byte(s) to string
            final_str = bits_toStr.rstrip()
        except ValueError:
            print("Error: temp_handler.py: TempSensor.get_temp - Check COM connection with Arduino")
            final_str = None
        finally:
            if final_str is not None:
                print("value read from port = ", final_str)
            return final_str

    def create_graph_dataset(self):  # Creates dataset compatible for flask/chart.js calls
        data_x_values = [None]*self.dataset_rows  # Data values for graph - x axis
        data_y_values = [None]*self.dataset_rows  # Data values for graph - y axis
        for i in range(self.dataset_rows):  # Create 2d array with datetime and temp values from arduino

            while True:  # Read MCU serial port until data arrives
                data_y_values[i] = self.get_data_serial_port()  # Grab data from MCU Serial port
                if data_y_values[i] is not None:  # Stay in loop until we get an actual value
                    # If a data line has been read from serial port, the next value will be the rpm
                    rpm_value = self.get_data_serial_port()
                    print("data value = " + data_y_values[i], "\t rpm value = " + str(rpm_value))
                    break
            curr_datetime = datetime.datetime.now()  # Grab current date and time
            format_datetime = curr_datetime.strftime("(%m/%d/%Y)-[%H:%M:%S]")  # Format datetime
            data_x_values[i] = format_datetime  # Create labels for x values in database
            time.sleep(self.serial_loop_freq)
        data = {"x_values": data_x_values,  # Create series for json conversion
                "y_values": data_y_values}
        json_data_temperature = json.dumps(data)  # Convert series to json data for flask/chart.js
        return json_data_temperature, rpm_value

    # def set_temp(self):  # TODO: Function that will take database values and pass via serial port to MCU ot utilize.


# Used for debugging purposes
# if __name__ == '__main__':
#     ts = TempSensor()
#     ts.create_graph_dataset()