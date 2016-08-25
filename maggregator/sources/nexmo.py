from .source import WebhookSource
from datetime import datetime
from flask import request

class NexmoSource(WebhookSource):
    def handle(self):
        self.save_message(
            request.args.get('text'),
            request.args.get('msisdn'),
            request.args.get('message-timestamp')
        )
        return ""


