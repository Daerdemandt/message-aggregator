from konf import Konf
from good import Schema, Optional, Extra, Reject, Invalid
from collections import Counter

import sources

#TODO: use messages to explain what's wrong in the config
#TODO: check that feed names and user names are unique
#TODO: check that only existing feeds are used in users
#TODO: check that only existing sources are used in feeds
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
    if len(all_sources) != len(set(all_sources)):
        counts = Counter(all_sources)
        reused_names = {source for source in all_sources if counts[source]  > 1}
        raise Invalid('Some source names are reused:' + ', '.join(reused_names))
    config['a'] = all_sources

    return config

