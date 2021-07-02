from flask import Flask
import time


class FlaskClass(object):
    def __init__(self):
        self.appHandle = Flask(__name__)

    def start_Flask(self):
        # @self.appHandle.route("/")
        return "Test"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = FlaskClass()
    @app.appHandle.route("/")
    def hello():
        return "This is a test"

    app.start_Flask()
    hello()
    while(True):
        time.sleep(1)
    print("End")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
