from .source import *
from .test import *

by_config_name = {
    'test source' : TestSource,
    'webhook test source' : WebhookTestSource,
    'on demand test source' : OndemandTestSource
}

def spawn(source_list, persistence):
    all_sources = {}
    for source_type, sources in source_list.items():
        cls = by_config_name[source_type]
        for source_name, config_params in sources.items():
            params = {
                **config_params,
                'name' : source_name,
                'persistence' : persistence
            }
            source = cls(**params)
            all_sources[source_name] = source
    return all_sources

