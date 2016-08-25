from .source import WebhookSource
from datetime import datetime
from flask import request

class NexmoSource(WebhookSource):
    def handle(self):
        if not request.args.get('message-timestamp'):
            # This is not actually a message, nexmo is just checking if address is OK
            return ""
        self.save_message(
            request.args.get('text'),
            request.args.get('msisdn'),
            request.args.get('message-timestamp')
        )
        return ""


