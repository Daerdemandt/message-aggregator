from .source import WebhookSource, OndemandSource
from datetime import datetime
from flask import request

class WebhookTestSource(WebhookSource):
    def handle(self):
        if 'X-Forwarded-For' in request.headers:
            remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
        else:
            remote_addr = request.remote_addr or 'untrackable'
        self.save_message('Webhook-triggered message from ' + self.name, remote_addr, 'now')
        return ""

class OndemandTestSource(OndemandSource):
    def fetch_new(self, since):
       return [{
            'message' : 'On-demande generated message from ' + self.name,
            'sender' : 'time itself',
            'time' : 'now'
        }]
