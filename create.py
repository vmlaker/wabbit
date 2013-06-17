"""Create MySQL user and database, as configured in wabbit.cfg file."""

from coils import user_input, Config
from sqlalchemy import create_engine

config = Config('wabbit.cfg')

# Connect to database engine.
root_u = user_input('Admin username', default=config['admin'])
root_p = user_input('Admin password', password=True)
engine = create_engine(
    'mysql://{}:{}@{}'.format(root_u, root_p, config['host']))
conn = engine.connect()

# Create the database and user.
try:
    conn.execute('CREATE DATABASE {}'.format(config['db_name']))
    conn.execute('CREATE USER "{}"@"{}" IDENTIFIED BY "{}"'.format(
            config['username'], config['host'], config['password']))
    conn.execute('GRANT ALL ON `{}`.* TO "{}"@"{}"'.format(
            config['db_name'], config['username'], config['host']))
except: 
    print('Failed to create.')

# Disconnect from database engine.
conn.close()
