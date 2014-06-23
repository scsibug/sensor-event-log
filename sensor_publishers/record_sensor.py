#!/usr/bin/python
# Example of writing a sensor value to a remote sensor event log server.
import sys
import hmac
import hashlib
import json
import decimal
import urllib2
import time
import argparse
import os

print "using "+os.environ['EVENT_SECRET_KEY']
parser = argparse.ArgumentParser(description='Write sensor value to remote server.')
parser.add_argument('--host', help='remote host to send updates to')
parser.add_argument('--monitor', help='name of monitor producing the sensor event')
parser.add_argument('reading', help='numeric reading from the sensor')

args = parser.parse_args()
data = json.dumps({"type": "float", "value": args.reading, "monitor": args.monitor, "time": time.time()})
print data
authz = "HMAC "+hmac.new(os.environ['EVENT_SECRET_KEY'],data,hashlib.sha256).hexdigest()
print "computed authz: "+authz
req = urllib2.Request(args.host, data, {'Content-Type': 'application/json', 'Authorization': authz})
f = urllib2.urlopen(req)
response = f.read()
print response
f.close()
