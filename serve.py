"""
Flask server app.
"""

import datetime as dt
import sys
import flask
import sqlalchemy as sa
import coils
import tables
import mapping

app = flask.Flask(__name__)

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

@app.route('/')
def index():
    """Render the index page."""
    return flask.render_template('index.html')    

@app.route('/info')
def info():
    """Return JSON of server info."""
    # Connect to database engine.
    engine = sa.create_engine(
        'mysql://{}:{}@{}/{}'.format(
            config['username'], config['password'],
            config['host'], config['db_name']))
    Session = sa.orm.sessionmaker(bind=engine)
    session = Session()
    now = dt.datetime.now()
    datum = session.query(mapping.Datum).\
        filter(mapping.Datum.name=='size')[0]
    return flask.jsonify(server_time=now, db_size=datum.value)

if __name__ == '__main__':
    app.run()
