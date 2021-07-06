# Create relational database that is sql based, lightweight and can be embedded into a python application.
import sqlite3
import WebMonitor.Hardware.temp_handler as tmp
import time


# SQL_lite-based class that will be used to store our sensor data types into a relational database
class WriteDatabase(object):
    # def __init__(self):
        # self.conn = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
        # self.cur = self.conn.cursor()  # Cursor used to make all operations with the database
        # self.temp_handle = tmp.TempSensor()
        # self.setup_database = False
        # self.sentinel_loop = False  # Sentinel flag used to drive data loops

    def setup(self):  # Configure database
        # Create tables/setup database  # TODO: Check to see if database exists - if so, do not execute
        try:
            connection = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS sensor_data (temp_data text)')
            connection.commit()  # Push changes to database
            # self.setup_database = True  # Flag to ensure database has been properly setup
            # self.sentinel_loop = True  # Ensure that all loops in database class are ready
            connection.close()
        except sqlite3.OperationalError as e:
            print(e)

    def get_dataset(self, temp_handle):  # Grabs dataset values from temp_handler
        # if not self.setup_database:  # Setup database if the call has not already been made.
        #     self.setup()
        # temp_handle = tmp.TempSensor()
        dataset_values = temp_handle.create_graph_dataset()
        return dataset_values

    def store_data_db(self):  # Grabs data from MCU and stores it into specific table within the database
        # if not self.setup_database:  # Setup database if the call has not already been made.
        #     self.setup()
        self.setup()
        temp_handle = tmp.TempSensor()
        while True:  # TODO: Pass flag thru thread
            connection = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
            cursor = connection.cursor()
            dataset = self.get_dataset(temp_handle)
            cursor.execute("INSERT INTO sensor_data (temp_data) VALUES (?)", (dataset,))  # Store actual data
            connection.commit()  # Push changes to database
            connection.close()

    # def close_db(self):  # Deallocate any resources/close database
    #     if self.conn or self.cur:  # If connection, close database
    #         try:
    #             self.conn.close()
    #             self.cur.close()
    #         except Exception as e:
    #             print(e)


def read_data_db():  # Reads data from the database
    connectDB = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
    cursor = connectDB.cursor()  # Cursor used to make all operations with the database
    # Grab the most recent dataset inside of the database - we want our UI to show the most recent data.
    cursor.execute('SELECT * FROM sensor_data ORDER BY temp_data DESC LIMIT 1')
    getData = cursor.fetchall()
    connectDB.close()  # Close connection
    return getData


# class ReadDatabase(object):
#     def __init__(self):
#         self.db_name = 'temperature_datasets.db'


# Used to for testing/troubleshooting purposes
# if __name__ == '__main__':
#     # db = Database()
#     db.setup()
#     for i in range(10):
#         # db.read_db_dataset()
#         db.store_data()
#     db.read_db_dataset()
#     db.close_db()
