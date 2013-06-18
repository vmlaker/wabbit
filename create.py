"""Create MySQL database and user."""

import sys
from sqlalchemy import create_engine
from coils import user_input, Config

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = Config(CONFIG)

# Connect to database engine.
root_u = user_input('Admin username', default=config['admin'])
root_p = user_input('Admin password', password=True)
engine = create_engine(
    'mysql://{}:{}@{}'.format(root_u, root_p, config['host']))
conn = engine.connect()

# Create the database and user.
try:
    conn.execute('CREATE DATABASE {}'.format(config['db_name']))
except: 
    print('Failed to create database.')
try:
    conn.execute('CREATE USER "{}"@"{}" IDENTIFIED BY "{}"'.format(
            config['username'], config['host'], config['password']))
    conn.execute('GRANT ALL ON `{}`.* TO "{}"@"{}"'.format(
            config['db_name'], config['username'], config['host']))
except: 
    print('Failed to create user.')

# Disconnect from database engine.
conn.close()
