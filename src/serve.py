"""
Flask server app.
"""

import os
import datetime as dt
import sys
import flask
from flask.ext.sqlalchemy import SQLAlchemy
import coils
import mapping


# Load the configuration file.
config = coils.Config('wabbit.cfg')

# Initialize Flask and SQLAlchemy.
app = flask.Flask(
    __name__,
    template_folder=config['flask_template_dir'],
    static_folder=config['flask_static_dir'],
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(
    config['username'], config['password'],
    config['host'], config['db_name'])
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Render the index page."""
    return flask.render_template('index.html')    

@app.route('/info')
def info():
    """Return system information."""
    now = dt.datetime.now()
    now = coils.time2string(now)
    size = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='size')[0]
    latest_tstamp = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='latest_tstamp')[0]
    latest_url = coils.time2fname(
        coils.string2time(
            latest_tstamp.value), full=True)
    latest_url = 'pics/{}.{}'.format(latest_url, config['f_ext'])
    load_avg = os.getloadavg()
    return flask.jsonify(
        server_time=now, 
        db_size=size.value, 
        latest_tstamp=latest_tstamp.value,
        latest_url=latest_url,
        load_avg='{:.2f}, {:.2f}, {:.2f}'.format(*load_avg),
        )

@app.route('/tstamps', methods = ['GET','POST'])
def tstamps():
    """Return timestamps within given range."""

    # Parse the URL parameters "begin" and "length".
    errors = list()
    try:
        begin = flask.request.args.get('begin')
        t_begin = coils.string2time(begin)
        assert t_begin != None
    except:
        errors.append('Failed to parse "begin" parameter.')
    try:
        length = int(flask.request.args.get('length'))
    except:
        errors.append('Failed to parse "length" parameter.')

    # Bail on any errors.
    if errors:
        return flask.jsonify(errors=errors)

    # Compute the end time.
    t_end = t_begin + dt.timedelta(seconds=length) if length > 0 else dt.datetime.now()

    # Retrieve image timestamps.
    images = db.session.query(mapping.Image.time).\
        filter(mapping.Image.time > t_begin).\
        filter(mapping.Image.time < t_end).\
        group_by(mapping.Image.time).all()
    images = [ii[0] for ii in images]

    return flask.jsonify(
        size=len(images),
        images=images,
        )

@app.route('/slide', methods = ['GET','POST'])
def slide():
    """Return image of given slider time."""
    
    # Time this functions.
    timer = coils.Timer()

    # Parse the URL parameter "time".
    errors = list()
    try:
        query = flask.request.args.get('time1')
        tstamp1 = coils.string2time(query)
        assert tstamp1 != None
    except:
        errors.append('Failed to parse "time1" parameter.')

    try:
        query = flask.request.args.get('time2')
        tstamp2 = coils.string2time(query)
        assert tstamp2 != None
    except:
        errors.append('Failed to parse "time2" parameter.')

    try:
        query = flask.request.args.get('amount')
        amount = float(query)
    except:
        errors.append('Failed to parse "amount" parameter.')

    # Bail on any errors.
    if errors:
        return flask.jsonify(errors=errors)

    # Compute target time.
    diff = (tstamp2 - tstamp1).total_seconds()
    delta = dt.timedelta(seconds=diff*amount)
    tstamp3 = tstamp1 + delta

    # Get time closest to target time.
    result_time = getNearestTime(tstamp3)

    # Convert time to url.
    if result_time:
        result_url = coils.time2fname(coils.string2time(result_time), full=True)
        result_url = 'pics/{}.{}'.format(result_url, config['f_ext'])
    else:
        result_url = None

    return flask.jsonify(
        result_time=result_time,
        result_url=result_url,
        elapsed=timer.get().total_seconds(),
        )


@app.route('/nearest', methods = ['GET','POST'])
def nearest():
    """Return timestamp nearest to given time."""

    # Time this functions.
    timer = coils.Timer()

    # Parse the URL parameter "time".
    errors = list()
    try:
        tstamp_query = flask.request.args.get('time')
        time_query = coils.string2time(tstamp_query)
        assert time_query != None
    except:
        errors.append('Failed to parse "time" parameter.')

    # Bail on any errors.
    if errors:
        return flask.jsonify(errors=errors)
        
    return flask.jsonify(
        result=getNearestTime(time_query),
        elapsed=timer.get().total_seconds(),
        )

@app.route('/range', methods = ['GET','POST'])
def range():
    """Return timestamp range of given amount (since latest.)"""

    # Time this functions.
    timer = coils.Timer()

    # Parse the URL parameter "amount".
    errors = list()
    try:
        amount = flask.request.args.get('amount')
        amount = float(amount)
    except:
        errors.append('Failed to parse "amount" parameter.')

    # Bail on any errors.
    if errors:
        return flask.jsonify(errors=errors)


    latest_tstring = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='latest_tstamp')[0].value
    latest_time = coils.string2time(latest_tstring)
    start_time = latest_time - dt.timedelta(seconds=amount)
    start_tstring = getNearestTime(start_time)
    
    return flask.jsonify(
        begin_time=start_tstring,
        end_time=latest_tstring,
        )

def getNearestTime(time_query):
    """Given a datetime object, return the nearest time in 
    the database (in string format), or None if empty."""

    # Convert datetime object to string, for lookup in database.
    tstamp_query = coils.time2string(time_query)

    # Retrieve image timestamps.
    try:
        tstamp_left = db.session.query(mapping.Image.time).\
            filter(mapping.Image.time <= tstamp_query).\
            order_by(mapping.Image.time.desc()).limit(1)
        tstamp_left = tstamp_left[0].time
        delta_left = abs(coils.string2time(tstamp_left) - time_query)
    except:
        tstamp_left = None
        delta_left = dt.timedelta.max
        
    try:
        tstamp_right = db.session.query(mapping.Image.time).\
            filter(mapping.Image.time >= tstamp_query).\
            order_by(mapping.Image.time).limit(1)
        tstamp_right = tstamp_right[0].time
        delta_right = abs(coils.string2time(tstamp_right) - time_query)
    except:
        tstamp_right = None
        delta_right = dt.timedelta.max
        
    # The nearest value has the smallest delta from the query.
    result = tstamp_left if (delta_left < delta_right) else tstamp_right
    return result

if __name__ == '__main__':
    app.run()
