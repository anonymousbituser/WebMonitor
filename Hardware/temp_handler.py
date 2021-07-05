import serial
import time


class TempSensor(object):
    def __init__(self):
        self.temp = 0;
        self.serial_port = 'COM3'   # Specific serial port connected to Arduino
        self.baud_rate = 9600       # Baud rate used on specific com port
        self.serialHandle = serial.Serial(self.serial_port, self.baud_rate)  # Initialize com port

    def get_temp(self):  # Grab temperature value from serial port of Arduino
        try:
            recv_bits = self.serialHandle.readline()
            bits_toStr = recv_bits.decode()  # Convert raw byte(s) to string
            final_str = bits_toStr.rstrip()
            print(final_str)
        except ValueError:
            print("Error: temp_handler.py: TempSensor.get_temp - Check COM connection with Arduino")
            final_str = None
        finally:
            return final_str


# Used for debugging purposes
if __name__ == '__main__':
    ts = TempSensor()
    while True:
        ts.get_temp()
        time.sleep(1)