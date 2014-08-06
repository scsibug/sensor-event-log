from flask import Flask, request, g, abort
import os
import sys
import hmac
import hashlib
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
import logging
import json
import decimal

# Load config from environment

## PG_CONN
# expected value: 'dbname=sensorcollector user=sensorcollector password=sensorcollector host=localhost'
## APP_DEBUG 
# expected value: "true" (case-insensitive) to enable debug, any other
# value or unset to disable debugging.
## SECRET_SESSION_KEY
# secret key for session signing.

app = Flask("sensor-collector")
app.config.update(dict(
    DEBUG=os.environ.get("DEBUG","false")=="true".lower(),
    SECRET_KEY=os.environ.get("SECRET_SESSION_KEY", 'development key'),
    PG_CONN = os.environ.get("PG_CONN")
))

dbpool = None

# On startup: 
# * initialize a backend
# * enumerate the list of known agents
# * enumerate all the known sensors


def get_db():
    global dbpool
    conn = getattr(g, 'conn', None)
    if conn is None:
        g.conn = dbpool.getconn()
        app.logger.info("Got database connection")
    return conn

@app.teardown_appcontext
def teardown_db(exception):
    global dbpool
    conn = getattr(g, 'conn', None)
    if conn is not None:
        app.logger.info("returning connection to pool")
        dbpool.putconn(conn)
        g.conn = None

@app.before_first_request
def setup_logging():
    fh = logging.StreamHandler()
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(fh)
    app.logger.setLevel(logging.INFO)
    app.logger.info("before first request")

@app.before_first_request
def setup_db_pool():
    global dbpool
    app.logger.info("setting up db pool...")
    dbpool = psycopg2.pool.ThreadedConnectionPool(1,10, dsn=app.config['PG_CONN'])
    app.logger.info("finished setting up pool")

@app.route("/status", methods=['GET'])
def status():
    get_db()
    app.logger.info("logging for first request")
    return "Looking Good!"

if __name__ == '__main__':
    app.run(host="0.0.0.0")
