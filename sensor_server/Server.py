#!/usr/bin/python

import sys
import hmac
import hashlib
from flask import Flask, request, g
import psycopg2

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SENSOR_SERVER_SETTINGS', silent=True)

@app.route("/EventSink", methods=['POST'])
def add_event():
    app.logger.debug("event sink triggered")
    
#         #log.msg("event sink request received")
#         h = request.requestHeaders.getRawHeaders("Authorization", None)
#         # Check if Authorization header exists
#         if (not h):
#             #log.msg("request did not contain Authorization header...rejecting")
#             request.setResponseCode(401)
#             return "Missing HMAC in Authorization header"
#         # Check if Authorization header is valid
#         message = request.content.getvalue()
#         correct_hmac = "HMAC " + hmac.new("the-key", message, hashlib.sha256)
#         if (h != correct_hmac):
#             #log.msg("Authorization through HMAC failed")
#             request.setResponseCode(403)
#             return "HMAC in Authorization header not valid"
#         return "worked!"
