#!/usr/bin/python
from fluent import sender

# for local fluent
sender.setup('app')

from fluent import event
import time
while True:
    # Send a message every 500us 
    time.sleep(1.0)
    # send event to fluentd, with 'app.follow' tag
    event.Event('test', {
            'value': '23423'
            })
    print "send message"
