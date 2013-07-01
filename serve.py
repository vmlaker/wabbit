"""
Flask server app.
"""

import datetime as dt
import sys
import flask
import sqlalchemy as sa
import coils
import tables

app = flask.Flask(__name__)

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Connect to database engine.
engine = sa.create_engine(
    'mysql://{}:{}@{}/{}'.format(
        config['username'], config['password'],
        config['host'], config['db_name']))

@app.route('/')
def index():
    """Render the index page."""
    return flask.render_template('index.html')    

@app.route('/info')
def info():
    """Return JSON of server info."""
    now = dt.datetime.now()
    ss = sa.sql.select([sa.func.count()]).select_from(tables.image)
    conn = engine.connect()
    count = conn.execute(ss).scalar()
    return flask.jsonify(server_time=now, db_size=count)

@app.route('/list')
def root():
    """Return HTML list of all elements."""
    result = ''
    ss = sa.sql.select([tables.image])
    conn = engine.connect()
    rows = conn.execute(ss)
    for row in rows:
        result += '{:s}<br>'.format(row)
    return result

if __name__ == '__main__':
    app.run()
