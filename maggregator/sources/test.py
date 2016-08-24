from .source import Source, WebhookSource, OndemandSource
from datetime import datetime
from flask import request

class TestSource(Source):
    config_validators = {'stub_message':str}
    def __init__(self, name, description, stub_message, persistence):
        self.stub_message = stub_message
        super().__init__(name, description, persistence)

    @classmethod
    def get_config_validators(cls):
        return {
            **super().get_config_validators(),
            'stub_message' : str
        }

class WebhookTestSource(WebhookSource):
    config_validators = {'stub_message':str}
    def __init__(self, name, description, stub_message, persistence):
        self.stub_message = stub_message
        super().__init__(name, description, persistence)

    @classmethod
    def get_config_validators(cls):
        return {
            **super().get_config_validators(),
            'stub_message' : str
        }

    def handle(self):
        if 'X-Forwarded-For' in request.headers:
            remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
        else:
            remote_addr = request.remote_addr or 'untrackable'
        self.save_message(self.stub_message, remote_addr, 'now')
        return ""

class OndemandTestSource(OndemandSource):
    config_validators = {'stub_message':str}
    def __init__(self, name, description, stub_message, persistence):
        self.stub_message = stub_message
        super().__init__(name, description, persistence)

    @classmethod
    def get_config_validators(cls):
        return {
            **super().get_config_validators(),
            'stub_message' : str
        }

    def fetch_new(since):
       return [self.stub_message] 
