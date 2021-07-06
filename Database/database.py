# Create relational database that is sql based, lightweight and can be embedded into a python application.
import sqlite3
import WebMonitor.Hardware.temp_handler as tmp


# SQL_lite-based class that will be used to store our sensor data types into a relational database
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
        self.cur = self.conn.cursor()  # Cursor used to make all operations with the database
        self.temp_handle = tmp.TempSensor()
        self.setup_database = False

    def setup(self):  # Configure database
        # Create tables/setup database  # TODO: Check to see if database exists - if so, do not execute
        try:
            self.cur.execute('CREATE TABLE IF NOT EXISTS sensor_data (temp_data text)')
            self.conn.commit()  # Push changes to database
            self.setup_database = True  # Flag to ensure database has been properly setup
        except sqlite3.OperationalError as e:
            print(e)

    def store_data(self):
        dataset = self.get_dataset()
        # dataset = '74.5'
        print(dataset)
        self.cur.execute("INSERT INTO sensor_data (temp_data) VALUES (?)", (dataset,))  # Store actual data
        self.conn.commit()  # Push changes to database

    def get_dataset(self):  # Grabs dataset values from temp_handler
        if not self.setup_database:  # Setup database if the call has not already been made.
            self.setup()

        dataset_values = self.temp_handle.create_graph_dataset()
        return dataset_values

    def close_db(self):  # Deallocate any resources/close database
        if self.conn or self.cur:  # If connection, close database
            try:
                self.conn.close()
                self.cur.close()
            except Exception as e:
                print(e)


# Used to for testing/troubleshooting purposes
if __name__ == '__main__':
    db = Database()
    db.setup()
    db.store_data()
    db.close_db()
