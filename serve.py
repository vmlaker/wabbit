import sys
import flask
import sqlalchemy as sa
import coils
import tables

app = flask.Flask(__name__)

@app.route('/')
def root():

    # Load configuration file.
    CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
    config = coils.Config(CONFIG)

    # Connect to database engine.
    engine = sa.create_engine(
        'mysql://{}:{}@{}/{}'.format(
            config['username'], config['password'],
            config['host'], config['db_name']))
    conn = engine.connect()

    # Select and print.
    result = ''
    s = sa.sql.select([tables.image])
    rows = conn.execute(s)
    for row in rows:
        result += '{:s}<br>'.format(row)

    # Close the session.
    conn.close()
    return result

@app.route('/pics')
def pics():
    return 'Pictures!'

if __name__ == '__main__':
    app.run()
