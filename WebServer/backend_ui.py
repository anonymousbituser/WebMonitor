# This file will utilize a python-based web framework called Flask to call javascript APIs for web-based UI's
# TODO: Wrap this script into a class to allow for higher level calls/threading in other scopes of the application
from flask import Flask, jsonify, render_template, request
from data_handler import ManageData as md
import json

app = Flask(__name__)   # Class handle to call Flask API
data_manager = md()     # Main class used to create data management
data_manager.create_data_flow()   # Create data generator


# Decorator function - wraps a function for Flask to operate - maps url to return value
@app.route('/', methods=['GET'])
def main_page():
    tempData = [  # TODO: Temperature data - use dummy data until function calls to Arduino are implemented
        ("07-03-2021", 75.5),
        ("07-04-2021", 76.5),
        ("07-05-2021", 77.5),
        ("07-06-2021", 76.5),
        ("07-07-2021", 75.5),
        ("07-08-2021", 49.5),
    ]
    #  Parse out data to be returned and rendered into html/javascript for chart graph on flask web page
    line_labels = [row[0] for row in tempData]
    line_values = [row[1] for row in tempData]
    # Initialize chart.js based graph 
    return render_template("graph.html", labels=line_labels, values=line_values)


@app.route('/get_data', methods=['GET'])  # Grabs data from flask app
def get_data():
    # jsonstring_temperature_data, rpm_data = data_manager.get_data_from_db()  # Grab data from database
    data = data_manager.get_data_from_db()  # Grab data from database
    json_data = json.loads(data[0][0])
    return json_data
    # python_dict_convert = json.loads(jsonstring_temperature_data[0][0])
    # print(python_dict_convert)
    # python_dict_convert["rpm_value"] = [rpm_data[0][0], rpm_data[0][0], rpm_data[0][0], rpm_data[0][0], rpm_data[0][0], rpm_data[0][0]]
    # print(python_dict_convert)



    # new_dataset = json.dumps(python_dict_convert)
    # new_dataset = python_dict_convert



    # print(new_dataset)
    # rpm_dataset = {"rpm_value": rpm_data[0][0]}
    # print(rpm_dataset)
    # parse_json_rpm = json.loads(rpm_dataset)
    # new_dataset = parse_json_rpm.update(jsonstring_temperature_data[0][0])
    # print(new_dataset)
    # return new_dataset
    # return jsonstring_temperature_data[0][0]


# Used to for testing/troubleshooting purposes
if __name__ == '__main__':
    app.run(debug=True)  # Main entry point - start webserver
