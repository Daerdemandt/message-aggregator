from flask import Flask, abort, request
from config import parse
from sources import spawn
from persistence import makedb
from bson.json_util import dumps

config = parse('config.yml')

app = Flask(__name__)

persistence = makedb() # TODO: read stuff from config
sources = spawn(config['sources'], persistence)
feeds = {
    feed_name:{
        **feed,
        'sources':{sources[source_name] for source_name in feed['sources']},
        'source_names': [*feed['sources']]
    }
    for feed_name, feed in config['feeds'].items()
}
users = config['users']

@app.route('/webhooks/<source>')
def handle_webhook(source):
    if source in sources:
        try:
            return sources[source].handle()
        except AttributeError:
            pass
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
    if feedname not in feeds:
        abort(404)
    feed = feeds[feedname]
    # TODO: proper auth
    user = request.args.get('user')
    if user not in users or feedname not in users[user]['feeds']:
        abort(403)

    for source in feed['sources']:
        try:
            source.refresh()
        except AttributeError:
            pass

    res = persistence.messages.find({'source': {'$in': feed['source_names']}})
    return dumps(list(res))

if __name__ == "__main__":
    app.run(host='0.0.0.0', **config['server'])
