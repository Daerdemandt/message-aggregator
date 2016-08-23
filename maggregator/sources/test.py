from .source import Source

class TestSource(Source):
    config_validators = {'stub_message':str}
    def __init__(self, name, description, stub_message):
        self.stub_message = stub_message
        super().__init__(name, description)

    @classmethod
    def get_config_validators(cls):
        return {
            **super().get_config_validators(),
            'stub_message' : str
        }
