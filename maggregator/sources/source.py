from abc import ABCMeta, abstractmethod
from good import Schema

class Source(metaclass=ABCMeta):
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def save_message(message, sender, datetime):
        # name would be taken from self.name
        pass
    @classmethod
    def get_config_validators(cls):
        return {
            'description':str
        }


class OndemandSource(Source):
    def __init__(self, name, description, minimal_refresh_delay):
        self.delay = minimal_refresh_delay
        super().__init__(name, description)

    @abstractmethod
    def fetch_new(since):
        pass

    def refresh():
        # TODO: adapt this to be parallel-safe?
        # check if minimal_refresh_delay has passed since latest fetch
        # return if it has not
        latest_fetch = None
        for message in self.ferch_new(latest_access):
            self.save_message(**message)
        # update latest_fetch

class WebhookSource(Source):
    @abstractmethod
    def handle():
        pass

