"""
Flask server app.
"""

import datetime as dt
import sys
import flask
from flask.ext.sqlalchemy import SQLAlchemy
import coils
import mapping

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Initialize Flask and SQLAlchemy.
app = flask.Flask(__name__)
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
    size = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='size')[0]
    last_tstamp = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='last_tstamp')[0]
    last_url = coils.time2fname(
        coils.string2time(
            last_tstamp.value), full=True)
    last_url = 'pics/{}.{}'.format(last_url, config['f_ext'])
    return flask.jsonify(
        server_time=now, 
        db_size=size.value, 
        last_tstamp=last_tstamp.value,
        last_url=last_url,
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

if __name__ == '__main__':
    app.run()
