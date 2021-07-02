from flask import Flask
import time

app = Flask(__name__)  # Class handle to call Flask API
@app.route('/')  # Decorator function - wraps a function for Flask to operate - maps url to return value
def main_page():
    return 'Chilly Dog Web Monitor'



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


