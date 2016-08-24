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
    def __init__(self, minimal_refresh_delay, **kwargs):
        self.delay = minimal_refresh_delay
        super().__init__(**kwargs)

    @abstractmethod
    def fetch_new(since):
        pass

    def refresh(self):
        # TODO: THIS IS NOT THREAD-SAFE
        latest_access = self.get_latest_access_time()
        time_delta = datetime.utcnow() - latest_access
        if time_delta.total_seconds() < self.delay:
            return
        for message in self.fetch_new(latest_access):
            self.save_message(**message)
        # TODO: this actually could lose a message if it happened after calculating time_delta, but before following line:
        self.persistence.status.update_one({'source' : self.name}, {'$set' : {'latest_access_time' : datetime.utcnow()}}, True)

    def get_latest_access_time(self):
        record = self.persistence.status.find_one({'source' : self.name})
        if record:
            return record['latest_access_time']
        return datetime.utcfromtimestamp(0)

    @classmethod
    def get_config_validators(cls):
        return {
            **super().get_config_validators(),
            'minimal_refresh_delay' : int,
        }



class WebhookSource(Source):
    @abstractmethod
    def handle(self):
        pass

