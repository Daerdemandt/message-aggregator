from konf import Konf
from good import Schema, Optional, Extra, Reject, Invalid
from collections import Counter

import sources

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


def parse(filename):
    k = Konf(filename)

    config = {
        'sources' : k('sources', is_valid_source_list),
        'feeds' : k('feeds', is_valid_feed_list),
        'users' : k('users', is_valid_user_list)
    }

    all_sources = [source for type_sources in config['sources'].values() for source in type_sources.keys()]
    sources_set = set(all_sources)
    if len(all_sources) != len(sources_set):
        counts = Counter(all_sources)
        reused_names = [source for source in sources_set if counts[source]  > 1]
        raise Invalid('Some source names are reused:' + ', '.join(reused_names))

    for feed_name, feed in config['feeds'].items():
        for source in feed['sources']:
            if source not in sources_set:
                raise Invalid('Unknown source "' + source + '" at feed "' + feed_name + '"')

    feeds = set(config['feeds'].keys())

    for username, user in config['users'].items():
        for feed in user['feeds']:
            if feed not in feeds:
                raise Invalid('Unknown feed "' + feed + '" at user "' + username + '"')

    return config

