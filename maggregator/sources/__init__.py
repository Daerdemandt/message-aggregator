from .source import *
from .test import TestSource

by_config_name = {
    'test source' : TestSource
}

def spawn(source_list):
    all_sources = []
    for source_type, sources in source_list.items():
        cls = by_config_name[source_type]
        for source_name, params in sources.items():
            params['name'] = source_name
            source = cls(**params)
            all_sources.append(source)
    result = {
        'all' : all_sources,
        'webhook' : [source for source in all_sources if isinstance(source, WebhookSource)],
        'ondemand' : [source for source in all_sources if isinstance(source, OndemandSource)]
    }
    return result

