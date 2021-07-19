# This file is responsible for managing data from and to the database via the webserver.

from WebMonitor.Database.database import *
import threading
import json


# Class that will manage the flow of data between each component of the system.
class ManageData(object):
    def __init__(self):  # Initialize the class with all necessary objects/variables
        # self.db = WriteDatabase()  # Object of class utilized to interact with the database.
        self.data_ready = False  # Flag used to indicate when data can be read from the database.

    def create_data_flow(self):  # Create data to be sent to the database, and allow other threads to read from the db
        generate_dataThread = threading.Thread(target=write_database)  # Create thread handle
        generate_dataThread.start()  # Start thread to send data from hardware to database
        self.data_ready = True  # Indicate that data can be read from the database

    def get_data_from_db(self):  # Grabs data from database
        if self.data_ready:
            # flaskData_temperature, flaskData_rpm = read_data_db()  # Grab dataset to be sent to flask framework
            data = read_data_db()  # Grab dataset to be sent to flask framework
        else:
            no_data = None
            # Ensure data is proper json string datatype in case data_ready is false.
            # flaskData_temperature = json.dumps(no_data)
            data = json.dumps(no_data)
        # return flaskData_temperature, flaskData_rpm
        return data

    # def query_client(self): # Grab data from flask app


# Used for debugging purposes
# if __name__ == '__main__':
#     md = ManageData()
#     md.create_data_flow()
#     # md.create_data_flow()
#     for i in range(10):
#         data = md.get_data_from_db()
#         print(data)
#         time.sleep(5)
#     # ts = TempSensor()
    # ts.create_graph_dataset()

