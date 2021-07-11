# Create relational database that is sql based, lightweight and can be embedded into a python application.
import sqlite3
import WebMonitor.Hardware.temp_handler as tmp


# SQL_lite-based class that will be used to store our sensor data types into a relational database
def setup():  # Configure database
    # Create tables/setup database
    try:
        connection = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
        cursor = connection.cursor()
        # Create string table for sensor data
        cursor.execute('CREATE TABLE IF NOT EXISTS sensor_data (temp_data text)')
        connection.commit()  # Push changes to database
        # Create integer table for fan data
        cursor.execute('CREATE TABLE IF NOT EXISTS fan_data (rpm text)')
        connection.commit()  # Push changes to database
        connection.close()
    except sqlite3.OperationalError as e:
        print(e)


def get_dataset(temp_handle):  # Grabs dataset values from temp_handler
    dataset_values = temp_handle.create_graph_dataset()
    # Break out tuple
    temperature = dataset_values[0]
    rpm = dataset_values[1]
    return temperature, rpm


def write_database():  # Grabs data from MCU and stores it into specific table within the database
    setup()  # Setup database if the call has not already been made.
    temp_handle = tmp.TempSensor()
    while True:  # TODO: Pass flag thru thread
        connection = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
        cursor = connection.cursor()
        temperature, rpm = get_dataset(temp_handle)
        cursor.execute("INSERT INTO sensor_data (temp_data) VALUES (?)", (temperature,))  # Store actual data
        connection.commit()  # Push changes to database
        cursor.execute("INSERT INTO fan_data (rpm) VALUES (?)", (rpm,))  # Store actual data
        connection.commit()  # Push changes to database
        connection.close()


def read_data_db():  # Reads data from the database
    connectDB = sqlite3.connect('temperature_datasets.db')  # Creates connection to database
    cursor = connectDB.cursor()  # Cursor used to make all operations with the database
    # Grab the most recent dataset inside of the database - we want our UI to show the most recent data.
    cursor.execute('SELECT * FROM sensor_data ORDER BY temp_data DESC LIMIT 1')
    get_temperature = cursor.fetchall()
    cursor.execute('SELECT * FROM fan_data ORDER BY rpm DESC LIMIT 1')
    get_rpm = cursor.fetchall()
    connectDB.close()  # Close connection
    return get_temperature, get_rpm


# Used to for testing/troubleshooting purposes
# if __name__ == '__main__':
#     # db = Database()
#     db.setup()
#     for i in range(10):
#         # db.read_db_dataset()
#         db.store_data()
#     db.read_db_dataset()
#     db.close_db()
