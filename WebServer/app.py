from flask import Flask, jsonify, render_template, request
import time
import random
import json

app = Flask(__name__)  # Class handle to call Flask API


@app.route('/', methods=['GET'])  # Decorator function - wraps a function for Flask to operate - maps url to return value
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
    return render_template("graph.html", labels=line_labels, values=line_values)
    #return render_template("graph.html")

@app.route('/get_data', methods=['GET'])  # Grabs data from flask app
def get_data():
    tempData_ran = [
        ("07-03-2021", random.random()),
        ("07-03-2021", random.random()),
        ("07-03-2021", random.random()),
        ("07-03-2021", random.random()),
        ("07-03-2021", random.random()),
        ("07-03-2021", random.random()),
    ]
    x_axis = [row[0] for row in tempData_ran]
    y_axis = [row[1] for row in tempData_ran]
    data = {"x_values": ['07-03-2021', '07-04-2021', '07-10-2021', '07-06-2021', '07-07-2021', '07-08-2021'],
            "y_values": [random.random()*100.0, random.random()*100.0, random.random()*100.0, random.random()*100.0,
                         random.random()*100.0, random.random()*100.0]}
    # data['x_values'] = []
    # data['x_values'].append(
    #     {
    #         '1': '07-03-2021',
    #         '2': '07-04-2021',
    #         '3': '07-05-2021',
    #         '4': '07-06-2021',
    #         '5': '07-07-2021',
    #         '6': '07-08-2021'
    #     }
    # )
    # data['y_values'] = []
    # data['y_values'].append(
    #     {
    #         'val': random.random()*100.0,
    #         '2': random.random()*100.0,
    #         '3': random.random()*100.0,
    #         '4': random.random()*100.0,
    #         '5': random.random()*100.0,
    #         '6': random.random()*100.0
    #     }
    # )
    json_dataString = json.dumps(data)
    # print(json_dataString)
    return json_dataString
    # return jsonify(tempData_ran)
    # return jsonify({'set_y_axis': y_axis}, {'set_x_axis': x_axis})
    # return tempData_ran
    # return jsonify(tempData_ran)  # Returns data into json format on route path
    # return render_template("graph.html", lab)
    # return render_template('graph.html')




# class FlaskClass(object):
#     def __init__(self):
#         self.appHandle = Flask(__name__)
#
#     def start_Flask(self):
#         # @self.appHandle.route("/")
#         return "Test"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)  # Main entry point - start web server
    # app = FlaskClass()
    # @app.appHandle.route("/")
    # def hello():
    #     return "This is a test"
    #
    # app.start_Flask()
    # hello()
    # while(True):
    #     time.sleep(1)
    # print("End")


