"""Create MySQL database and user."""

import sys
import sqlalchemy as sa
import coils
import tables

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Connect to database engine.
root_u = coils.user_input('Admin username', default=config['admin'])
root_p = coils.user_input('Admin password', password=True)
engine = sa.create_engine(
    'mysql://{}:{}@{}'.format(root_u, root_p, config['host']))
conn = engine.connect()

# Create the database and user.
try:
    conn.execute('CREATE DATABASE {}'.format(config['db_name']))
except sa.exc.ProgrammingError: 
    print('Failed to create database.')
try:
    conn.execute('CREATE USER "{}"@"{}" IDENTIFIED BY "{}"'.format(
            config['username'], config['host'], config['password']))
    conn.execute('GRANT ALL ON `{}`.* TO "{}"@"{}"'.format(
            config['db_name'], config['username'], config['host']))
except sa.exc.OperationalError:
    print('Failed to create user.')

# Disconnect from database engine.
conn.close()

# Create table.
e2 = sa.create_engine(
    'mysql://{}:{}@{}/{}'.format(
        root_u, root_p, config['host'], config['db_name']))
tables.metadata.create_all(e2)
print('Created table.')
