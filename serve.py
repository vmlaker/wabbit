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
    datum = db.session.query(mapping.Datum).\
        filter(mapping.Datum.name=='size')[0]
    return flask.jsonify(server_time=now, db_size=datum.value)

if __name__ == '__main__':
    app.run()
