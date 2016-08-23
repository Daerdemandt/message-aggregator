from flask import Flask, abort, request
from pprint import pformat
from config import parse
from sources import spawn

config = parse('config.yml')

app = Flask(__name__)

sources = spawn(config['sources'])

#TODO: check that this actually works
for source in sources['webhook']:
    @app.route('/webhooks/' + source.name)
    def handle():
        source.handle()

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
    # query the db
    return "nothing here yet"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
