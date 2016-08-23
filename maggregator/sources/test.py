from .source import Source, WebhookSource, OndemandSource

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
        self.save_message(self.stub_message, 'unknown', 'now')
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
