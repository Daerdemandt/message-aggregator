from flask import Flask, abort, request
from pprint import pformat
from config import parse
from sources import spawn
from persistence import makedb

config = parse('config.yml')

app = Flask(__name__)

persistence = makedb() # TODO: read stuff from config
sources = spawn(config['sources'], persistence)

@app.route('/webhooks/<source>')
def handle_webhook(source):
    if source in sources['webhook']:
        return sources['webhook'][source].handle()
    abort(404)

@app.route('/health')
def get_health():
    return "Ok"

#TODO: this is for debugging purposes only, remove
@app.route('/config')
def display_config():
    return pformat(config)

@app.route('/feeds/<feedname>')
def get_feed(feedname):
    if feedname not in config['feeds']:
        abort(404)
    # TODO: proper auth
    user = request.args.get('user')
    if user not in config['users'] or feedname not in config['users'][user]['feeds']:
        abort(403)
    # Poll ondemand sources
    for source in sources['ondemand']:
        source.refresh()
    res = persistence.messages.find()
    return pformat(list(res))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
