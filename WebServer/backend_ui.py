# This file will utilize a python-based web framework called Flask to call javascript APIs for web-based UI's
# TODO: Wrap this script into a class to allow for higher level calls/threading in other scopes of the application
from flask import Flask, jsonify, render_template, request
import random
import json

app = Flask(__name__)  # Class handle to call Flask API

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
    # Create temp data to use for flask graphing pipeline
    data = {"x_values": ['07-03-2021', '07-04-2021', '07-10-2021', '07-06-2021', '07-07-2021', '07-08-2021'],
            "y_values": [random.random()*100.0, random.random()*100.0, random.random()*100.0, random.random()*100.0,
                         random.random()*100.0, random.random()*100.0]}
    json_dataString = json.dumps(data)
    return json_dataString


# Used to for testing/troubleshooting purposes
if __name__ == '__main__':
    app.run(debug=True)  # Main entry point - start web server

