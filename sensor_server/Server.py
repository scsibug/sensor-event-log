from flask import Flask, request, g, abort
import sys
import hmac
import hashlib
import psycopg2
import logging
import json
import decimal

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='development key',
    EVENT_SECRET_KEY='demo-secret-key',
    PG_CONN = 'dbname=sensorcollector user=sensorcollector password=sensorcollector host=localhost'
))
app.config.from_envvar('SENSOR_SERVER_SETTINGS', silent=True)

# SQL queries
find_monitor_id_SQL = "select name,id from monitor_points"
insert_value_SQL = "insert into point_values (id, monitor_point, numeric_val, tstamp) values (DEFAULT, %(monitor_id)s, %(val)s, timestamptz 'epoch' + %(tstamp)s * INTERVAL '1 second')"

def connect_db():
    conn = psycopg2.connect(app.config['PG_CONN'])
    return conn

def get_db():
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'pg_db'):
        g.pg_db.close()

@app.before_first_request
def setup_logging():
    fh = logging.StreamHandler()
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(fh)
    app.logger.setLevel(logging.INFO)

def get_monitors():
    if not hasattr(g, 'monitors'):
        conn = get_db()
        curs = conn.cursor() 
        curs.execute(find_monitor_id_SQL)    
        monitors = dict(curs.fetchall())
        curs.close()
        g.monitors = monitors
    return monitors

@app.route("/EventSink", methods=['POST'])
def add_event():
    app.logger.info("event sink triggered")

    authz_header = request.headers.get('Authorization')
    if (authz_header == None):
        abort(401)
    # Compute hmac sha256 of request content
    correct_authz = "HMAC "+hmac.new(app.config['EVENT_SECRET_KEY'],request.data,hashlib.sha256).hexdigest()
    hmac_matched = False
    # python 2.7.7 required for compare_digest
    try:
        hmac_matched = hmac.compare_digest(authz_header, correct_authz)
    except AttributeError:
        app.logger.warn("falling back to insecure HMAC comparison (upgrade python to 2.7.7+!")
        hmac_matched = authz_header == correct_authz
    if (not hmac_matched):
        app.logger.warn("Mismatched HMAC, should have been "+correct_authz)
        abort(403)
    # Record event, now that we have verified it was correctly signed.
    conn = get_db()
    curs = conn.cursor() 
    monitors = get_monitors()
    app.logger.info(monitors)
    # Legacy values are sent as: {"float": "46.5", "monitor": "dajeil.SOC.temp.1", "time": 1403476561.889899}
    # tmp102 value *continues* to be coming across as a raw float, others are strings
    # desired format is:     {"type": "float", "value": "46.5", "monitor": "dajeil.SOC.temp.1", "time": 1403476561.889899}
    # Look at event... for now, assume type="float"
    reading = json.loads(request.data, parse_float=decimal.Decimal)
    app.logger.info("reading: "+str(reading))
    # This second parse is temporary, as some early values were loaded as strings, and this serves to strip them
    fv = decimal.Decimal(reading["value"])
    monitor = reading["monitor"].strip()
    epoch = reading["time"]
    monitor_id = decimal.Decimal(monitors[monitor])
    if monitor_id is None:
        app.logger.warn("Monitor not found: "+monitor)
        abort(400)
    print("Need to insert for monitor "+str(monitor_id)+" value "+str(fv))
    curs.execute(insert_value_SQL,{'monitor_id':monitor_id, 'val':fv, 'tstamp':epoch}) 
    conn.commit()
    curs.close()
    return "event recorded successfully"

if __name__ == '__main__':
    app.run(host="0.0.0.0")
