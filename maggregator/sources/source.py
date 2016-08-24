from abc import ABCMeta, abstractmethod
from good import Schema
from datetime import datetime
from dateparser import parse

class Source(metaclass=ABCMeta):
    def __init__(self, name, description, persistence):
        self.name = name
        self.description = description
        self.persistence = persistence
    def save_message(self, message, sender, time, metadata=None):
        if not isinstance(time, datetime):
            time = parse(time)
        self.persistence.messages.insert_one({
            'message' : message,
            'sender' : sender,
            'datetime' : time,
            'source' : self.name,
            'actual_datetime' : datetime.utcnow(),
            'metadata' : metadata
        })
    @classmethod
    def get_config_validators(cls):
        return {
            'description':str
        }


class OndemandSource(Source):
    def __init__(self, name, description, minimal_refresh_delay, persistence):
        self.delay = minimal_refresh_delay
        super().__init__(name, description, presistence)

    @abstractmethod
    def fetch_new(since):
        pass

    def refresh():
        # TODO: adapt this to be parallel-safe?
        # check if minimal_refresh_delay has passed since latest fetch
        # return if it has not
        latest_fetch = self.get_latest_access_time()
        for message in self.ferch_new(latest_access):
            self.save_message(**message)
        # update latest_fetch

    def get_latest_access_time(self):
        return None

class WebhookSource(Source):
    @abstractmethod
    def handle(self):
        pass

