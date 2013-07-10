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
    """Return JSON of server info."""
    now = dt.datetime.now()
    size = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='size')[0]
    last_tstamp = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='last_tstamp')[0]
    last_url = coils.time2fname(
        coils.string2time(
            last_tstamp.value), full=True)
    last_url = 'pics/{}.png'.format(last_url)
    return flask.jsonify(
        server_time=now, 
        db_size=size.value, 
        last_tstamp=last_tstamp.value,
        last_url=last_url,
        )

if __name__ == '__main__':
    app.run()
