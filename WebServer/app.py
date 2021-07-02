from flask import Flask, jsonify, render_template, request
import time

app = Flask(__name__)  # Class handle to call Flask API

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]


@app.route('/')  # Decorator function - wraps a function for Flask to operate - maps url to return value
def main_page():
    line_labels = labels
    line_values = values
    return render_template('graph.html', title='Chilly Dog Web Monitor', max=17000, labels=line_labels,
                           values=line_values)
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


