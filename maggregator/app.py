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

from good import Schema, Optional, Extra, Reject

import sources

#TODO: use messages to explain what's wrong in the config
is_valid_source_list = Schema(
    {
        name : {Extra : source.get_config_validators()}
        for (name, source)
        in sources.by_config_name.items()
    },
    default_keys=Optional
)

is_valid_feed_list = Schema({
    Extra: {
       'description' : str,
       'sources' : list
    }
})

is_valid_user_list =  Schema({
    Extra: {
       'description' : str,
       'feeds' : list
    }
})

#TODO: check that source names are unique even across different source types
#TODO: check that feed names and user names are unique
#TODO: check that only existing feeds are used in users
#TODO: check that only existing sources are used in feeds
#TODO: check for keyfile in user
#TODO: check session key expiration time

@app.route('/config')
def config():
    k = Konf('config.yml')

    r = {
        #'s' : k('sources', is_ok),
        'sources' : k('sources', is_valid_source_list),
        'f' : k('feeds', is_valid_feed_list),
        'u' : k('users', is_valid_user_list)
    }
    return pformat(r)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
