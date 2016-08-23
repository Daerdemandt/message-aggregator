import os
from pymongo import MongoClient
def makedb():
    client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
    return client.maggregator

class Persistence(object):
    def __init__(config):
        pass
    def get_feed(feedname):
        #TODO: move to a separate 'feed' class?
        pass
    def write_message(message, sender, datetime, source):
        pass
    def get_latest_access(source):
        pass


