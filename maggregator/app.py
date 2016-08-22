import os
from flask import Flask
from konf import Konf
from pprint import pformat
from validation import BetterSchema

app = Flask(__name__)


@app.route('/marco')
def marco():
    return "Polo!"

@BetterSchema
def is_ok(arg):
    return True

is_ok = is_ok & is_ok

@app.route('/config')
def config():
    k = Konf('config.yml')
    r = {
        's' : k('sources', is_ok),
        'f' : k('feeds', is_ok),
        'u' : k('users', is_ok)
    }
    return pformat(r)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
