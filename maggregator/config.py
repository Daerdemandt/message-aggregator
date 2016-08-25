from konf import Konf
from good import Schema, Optional, Extra, Reject, Invalid, Any, Fallback
from collections import Counter

import sources

#TODO: maybe use YAML sets for feeds in user and for sources in feeds? That makes more sense, but is more cumbersome
# Or maybe support both but convert to set anyway
#TODO: use messages to explain what's wrong in the config
#TODO: check for keyfile in user

#TODO: check session key expiration time
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

is_valid_server_conf = Schema({
    'port' : Any(int, Fallback(5000)),
    'debug' : Any(bool, Fallback(True))
})

def parse(filename):
    k = Konf(filename)

    # syntax
    config = {
        'server' : k('server', is_valid_server_conf),
        'sources' : k('sources', is_valid_source_list),
        'feeds' : k('feeds', is_valid_feed_list),
        'users' : k('users', is_valid_user_list)
    }

    # semantics
    # no duplicates:
    # TODO: move getting duplicates into a separate function
    all_sources = [source for type_sources in config['sources'].values() for source in type_sources.keys()]
    sources_set = set(all_sources)
    if len(all_sources) != len(sources_set):
        counts = Counter(all_sources)
        reused_names = [source for source in sources_set if counts[source]  > 1]
        raise Invalid('Some source names are reused:' + ', '.join(reused_names))

    for feed_name, feed in config['feeds'].items():
        feed['sources'] = set(feed['sources'])
        unknown_sources = feed['sources'] - sources_set
        if (unknown_sources):
            raise Invalid('Unknown sources at feed "' + feed_name + '": "' + ", ".join(unknown_sources) + '"')

    feeds = set(config['feeds'].keys())

    for username, user in config['users'].items():
        user['feeds'] = set(user['feeds'])
        unknown_feeds = user['feeds'] - feeds
        if (unknown_feeds):
            raise Invalid('Unknown feeds at user "' + username + '": "' + ", ".join(unknown_feeds) + '"')

    return config

