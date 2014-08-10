from flask import Flask, request, g, abort, jsonify
import os
import sys
import hmac
import hashlib
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
#from flask.ext.sqlalchemy import SQLAlchemy
import logging
import json
import decimal
import SensorStore

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
# Sensor Store
ss = None

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

@app.before_first_request
def sensor_store_setup():
    global dbpool
    global ss
    # All logic for working with the backend store is encapsulated in the SensorStore class.
    ss = SensorStore(app.config['PG_CONN'])

@app.before_first_request
def get_agent_credentials():
    # Retrieve the agents and their credentials, for use in authenticating readings
    c = get_conn()
    curs = c.cursor()
    curs.execute("SELECT name, signing_key FROM agents WHERE active=TRUE;")
    agent_rows = curs.fetchall()
    agents = []
    for agent in agent_rows:
        a = {'agent': agent[0],
             'key': agent[1]}
        agents.append(a)
    # iterate through the results to build a dictionary for conversion to JSON
    curs.close()
    

@app.route("/status", methods=['GET'])
def status():
    get_conn()
    app.logger.info("logging for first request")
    return "Looking Good!"

# Agents/sensors send their updates to: /agents/{AGENT}/sensors/{SENSOR}
# If a 404 is returned, that is the indication to the client that they should create the sensor.
# 200 indicates the reading was successfully saved (persisted)
# WHAT ABOUT updates to multiple sensors?  Do I have to do an HTTP POST for EVERY update? YES
@app.route("/agents/<agent>/sensors/<sensor>", methods=['POST'])
def create_reading(agent, sensor):
    return "Details for for %s:%s" % (agent,sensor)

@app.route("/agents/<agent>/sensors/<sensor>", methods=['GET'])
def describe_sensor(agent, sensor):
    # Get details for a specific sensor
    return jsonify(agent=agent,sensor=sensor)

# Sensor creation is accomplished through a POST to /agents/{AGENT}/sensors
@app.route("/agents/<agent>/sensors", methods=['POST'])
def create_sensor(agent):
    # Need to retrieve the agent secret key to validate.
    # Need to write a helper to authenticate a message!
    return "created sensor"

# Retrieve all agents.
# specify state=active or state=inactive to only view active/inactive agents, respectively
@app.route("/agents", methods=['GET'])
def agents():
    state = (True, False) # find active and inactive by default
    if ('state' in request.args):
      state = ((request.args['state'].lower() == "active"),)
    c = get_conn()
    curs = c.cursor()
    curs.execute("SELECT id, name, description, created, attr, active FROM agents WHERE active in %s ORDER by created;", (state,))
    agent_rows = curs.fetchall()
    agents = []
    for agent in agent_rows:
        a = {'name': agent[1],
             'description': agent[2],
             'created': mk_isodate(agent[3]),
             'attrs': agent[4],
             'active': agent[5]}
        agents.append(a)
    # iterate through the results to build a dictionary for conversion to JSON
    curs.close()
    return jsonify({'agents': agents})

def mk_isodate(d):
    if d is not None:
        return d.isoformat()
    else:
        return None

def authenticate_hmac(agent_name, body):
    return false

if __name__ == '__main__':
    app.run(host="0.0.0.0")
