# message-aggregator
Simple webservice to aggregate messages from various providers (especially sms gateways)

Supported sources:

+ [Nexmo](nexmo.com)
+ [smsc.ru](smsc.ru)

# Installation

+ Get the source :`git clone git@github.com:Daerdemandt/message-aggregator.git`
+ Edit `maggregator/config.yml` (by default, server wil listen on 5000 port and only run 2 test sources)
+ Run the service with Docker Compose: `cd message-aggregator; docker-compose up`
