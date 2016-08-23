import os
from flask import Flask
from pprint import pformat
import config

app = Flask(__name__)


@app.route('/marco')
def marco():
    return "Polo!"

@app.route('/config')
def display_config():
    r = config.parse('config.yml')

    return pformat(r)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
