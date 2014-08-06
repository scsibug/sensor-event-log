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
## PG_POOL_MAX
# max size of postgres connection pool.  Default is "10".
## APP_DEBUG 
# expected value: "true" (case-insensitive) to enable debug, any other
# value or unset to disable debugging.
## SECRET_SESSION_KEY
# secret key for session signing.

app = Flask("sensor-collector")
app.config.update(dict(
    DEBUG=os.environ.get("DEBUG","false")=="true".lower(),
    SECRET_KEY=os.environ.get("SECRET_SESSION_KEY", 'development key'),
    PG_CONN = os.environ.get("PG_CONN"),
    PG_POOL_MAX=int(os.environ.get("PG_POOL_MAX", '10'))
))

# Connection pool
dbpool = None

# On startup:
# * initialize database connection pool
# * enumerate the list of known agents
# * enumerate all the known sensors

def get_conn():
    global dbpool
    g.conn = getattr(g, 'conn', None)
    if g.conn is None:
        g.conn = dbpool.getconn()
    return g.conn

@app.teardown_appcontext
def teardown_db(exception):
    global dbpool
    conn = getattr(g, 'conn', None)
    if conn is not None:
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
    app.logger.info("Starting PG connection pool")
    dbpool = psycopg2.pool.ThreadedConnectionPool(1,app.config['PG_POOL_MAX'], dsn=app.config['PG_CONN'])

@app.route("/status", methods=['GET'])
def status():
    get_conn()
    app.logger.info("logging for first request")
    return "Looking Good!"

# Retrieve all active agents
@app.route("/agents", methods=['GET'])
def agents():
    # Query and display all the active agents
    c = get_conn()
    curs = c.cursor()
    curs.execute("SELECT name, description FROM agents WHERE active=TRUE");
    agents = dict(curs.fetchall())
    curs.close()
    return str(agents)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
