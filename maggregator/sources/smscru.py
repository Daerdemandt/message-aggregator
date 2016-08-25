from .source import OndemandSource
from datetime import datetime
from math import ceil
from urllib.request import urlopen
from urllib.error import URLError
import json
# TODO: test that this works
class SmscruSource(OndemandSource):
    """
    Adapter for working with smsc.ru API.

    Corresponding reference section can be found at https://smsc.ru/api/http/#inbox
    To check raw response from server, use following link:
    http://smsc.ru/sys/get.php?get_answers=1&login=<login>&psw=<password>&fmt=3&hour=100

    """
    @classmethod
    def get_config_validators(cls):
        return {
            **super().get_config_validators(),
            'login' : str,
            'password' : str,
        }
    def __init__(self, login, password, **kwargs):
        self.login = login
        self.password = password
        super().__init__(**kwargs)

    def fetch_new(self, since):
        time_elapsed = datetime.utcnow() - since
        hours = ceil(time_elapsed.total_seconds() / 3600)
        if hours < 1:
            hours = 1
        if hours > 168:
            hours = 168

        # fmt = 3 means response in json
        url = 'http://smsc.ru/sys/get.php?get_answers=1&login={login}&psw={password}&fmt=3&hour={hours}'.format(
            login = self.login,
            password = self.password,
            hours = hours
        )

        try:
            with urlopen(url) as resp:
                response = json.loads(resp.read().decode('utf-8'))
        except URLError:
            response = {} # TODO: log this and reflect in healthcheck

        def transform(msg):
            return {
                'message' : msg['message'],
                'sender' : msg['phone'],
                'time' : msg['sent']
            }

        return [transform(msg) for msg in response if datetime(msg['sent']) > since]
