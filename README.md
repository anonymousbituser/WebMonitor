# WebMonitor
 A web-based monitor that will analyze temperature values and set fan speeds based on defined temperature ranges.  This is the overall system that represents the project.
 ## Webserver 
 The webserver system component of the project is a python backend that is responisble for hosting the flask framework to display html objects onto a webpage.  The webserver will also retrieve data from the database.  The webserver will also create thread(s) to manage sending data into the database.
 ### data_handler.py
 This python source file is responsible for managing the data that comes to and from the database.
 #### class ManageData()
 This class utilizes functions from database.py to interact with the database.  This class will create the primary thread that will generate data by reading information from a specified serialport, and storing the data in proper datatypes into the database.
 ### backend_ui.py
 This python source file is responsible for performing the highest level operations of the program.  This source file will make the initial flask framework calls from the flask api and host the flask server on localhost port 5000. This file will use main_page() to initialize the web page by rendering our graph.html file - this will initialize the webpage when a user goes to the main website (http:\\localhost:5000).
 ### templates/graph.html
 This source file is responsible to using the chart.js api to generate a javascript-based chart for dynamic data display.  This file will also utilize jquery.js api to make ajax calls to the flask api in backend_ui.py, allowing the chart to be dynamically updated with new data from the database.
 ## Hardware
 The hardware system component of the project utilizes a series of hardware to take temperature measurements from a TM36 sensor, read RPM values from an F12 PWM PST fan, and set fan speeds based on temperature readings.  All of this data is then sent to the database.
 ### temp_handler.py
 This python source file is responsible for receiving data from the primary sub-system of the hardware system component, the Arduino microcontroller-based evaluation board.  This source file will utilize the python serial library to make calls to the serial port of the host that is connected to the Arduino.  All embedded measurements are retrieved from the serial port and stored into the database.
 #### class TempSensor()
 This class is responsible for retrieving data from the serial port and formatting it in a json string to then be stored properly into a specified table within our database.  The data is created into specific datasets of 6 temperature measurements, along with adjacent datetime points.  create_graph_dataset() will create all the datasets and return each set to be utilized by the webserver system component.
 ### temp_acquisition.ino
 This c++ based source file is responsible for utilizing the Arduino IDE and API to control the p328 microcontroller on the Arduino Uno R3 evaluation board. The setup() function utilizes the Arduino API to initialize the serial port of the eval. board, setup all digital and analog pins to be used in the webmonitor, and setup a interrupt service routine (ISR) that will use global timers on the microcontroller to properly measure tachometer signals from the fan - this will allow accurate measurements of rpm from the fan.
 ## Database
 The database system component of the project is responsible for storing all of the necessary data required for the webmonitor.  The database will use python's SQLite database, a lightweight local database that will create a simple .db database file for non-volatile memory of interest to be stored.  
 ### database.py
 This python source file is responsible for making the function calls to the database.  This file utilizes the sqlite3 python library to create the sql based relational database that is embedded into the webmonitor application itself, and does not require a separate independent server to run on the host and/or cloud services.
 ## Configuration Management
 A subsection of the project that will outline management of task tracking and controlling the changes made to the project.
 ### Development Tools
 A series of development tools utilized for creating the webmonitor
 #### Atom
 Open source text and source code editor utilized to edit the graph.html file.  This editor allowed intellisense for javascript code to be called within the .html file extension.
 #### Pycharm 2 - Community Edition
 Primary development tool utilized to select all of the python dependencies/interpreter/library and deploy the webserver environment in a local r&d environment.
 #### Firefox Developer Edition
 Browser used to diagnose all web-based operations of the webmonitor during development.
 #### Arduino IDE
 Responsible for programming the Arduino p328 microcontroller and diagnosing embedded operations of the Arduino used within the webmonitor.
 #### GitHub
 Version control for all software artifacts of the webmonitor.
 ## Current Status: 7/11/2021 (Assignment 4 - Development)
 Provide a status for Assignment 4 - Development.  All classes and methods called out in Assignment 3 are rather outlined above, or are within each system components respective source files.  Some methods exist within the source file per assignment 4's guidance, but are deprecated/commented out due to newly learned approaches and further understanding of technologies during current development process.  
 ### Percent Completion
 The project is currently at an 80% completion as of July 11th, 2021.  The webmonitor can run and display a dynamic graph on a webpage while retreiving data from a database, while synchronously capturing data from the embedded hardware and storing the information into the database.  The webmonitor can display the temperature on the graph, and the pwm fanspeed is dynamically controlled by the temperature readings of the microcontroller.  The database can store these temperature values, along with the rpm values, and the flask frontend can display the temperature value on the y axis of a chart, while graphing versus datetime in the x axis.  The graph is currently set to update every 10 seconds through an ajax call from jquerie's jquery.min.js javascript API.  The Arduino is set to make interrupt service routine calls every 1 second to take measurements of rpm and temperature, and then send the data over the serial port connected to the webserver host.  
 #### Functions
 All functions for completing the current estimated 80% project completion are outlined in the above headings, and are further documented inside each source file.  For the purpose of assignment 4, all functions/classes will be listed below:
 ##### main_page():  @app.route('/', methods=['GET']) Decorator function - wraps a function for Flask to operate - maps url to return value
 ##### get_data(): @app.route('/get_data', methods=['GET'])  # Grabs data from flask app 
 ##### class ManageData(object): Class that will manage the flow of data between each component of the system
 ##### ManageData.__init__(self):  # Initialize the class with all necessary objects/variables
 ##### ManageData.create_data_flow(self):  # Create data to be sent to the database, and allow other threads to read from the db
 ##### ManageData.get_data_from_db(self):  # Grabs data from database
 ##### function updateGraph() Ajax function that will be called to update the webpage with new data
 ##### class TempSensor(object): # Class used to read temp values from MCU over serial port
 ##### TempSensor.__init__(self): # Initialize the class with all necessary objects/variables
 ##### TempSensor.get_data_serial_port(self):  # Grab temperature value from serial port of Arduino
 ##### TempSensor.create_graph_dataset(self):  # Creates dataset compatible for flask/chart.js calls
 ##### setup():  # Configure database - Create tables/setup database
 ##### get_dataset(temp_handle):  # Grabs dataset values from temp_handler
 ##### write_database():  # Grabs data from MCU and stores it into specific table within the database
 ##### read_data_db():  # Reads data from the database
 ##### void setup(); // Initialization function  // Initialize serial port for testing/debugging
 ##### void get_rpm(); // Callback function that will increment to count every tick from rising edge - this will calculate the rpm.
 ##### void loop(); // Main loop to perform operations and grab data from sensor(s)
 ### Remaining Features/Efforts
The remaining feature that would be ideal to implement would be dynamic pwm duty cycle ranges mapped to temperature ranges.  Currently, the Arduino will turn on the fan power relays when 76° is reached, and will drive the pwm of the fan at a percentage of 0% to 100% from 76° to 80°.  A nice feature would be to allow the user to set the temperature min and max values for the "mapped" dynamic pwm percentage.  There exist all the infrastructure to do so - rpm measurements are captured by the hardware, sent to the database, and retrieved from flask.  The next steps are to create the proper html/javascript objects to display on the main webpage/userinterface and display rpm dynamically via the same ajax routine that updates the chart on the main page.
## Needed Environment
Anaconda 3.9 Python interpreter is needed in order to run the application. As long as the interpreter is installed on the host machine and is within the environment path, along with all of the libraries (further explained below), the application will run simply from a terminal, or a Python IDE that can access the interpreter. 
## Needed libraries/resources
All source files include all of the necessary libraries that are imported into each application. All required libraries can be installed with the following commands once Anaconda 3.9 Python interpreter is installed on the system:
### pip install flask
### pip install pyserial
### pip install sqlite3
### Arduino IDE
The user will need the Arduino IDE and to install TimeLib.h in order to compile and run the application on an Arduino Uno R3.  The user will also need a pulse width modulated +12v fan, along with an 8 channel 5v relay board - these hardware assets are required to receive data for the database.
## Process to run
Once all of the necessary libraries and resources above are present, the user can then access a terminal and type ./backend_ui.py, or run the same script inside of a Python IDE with the above mentioned interpreter, and the application will begin to run.  The embedded hardware will always run once the temp_acquisition.ino file is flashed onto the mcu of the Arduino.

