"""Create MySQL user and database, as configured in wabbit.cfg file."""

from coils import user_input, Config
from sqlalchemy import create_engine

config = Config('wabbit.cfg')

# Connect to database engine.
root_u = user_input('Admin username', default=config['admin'])
root_p = user_input('Admin password', password=True)
host = user_input('Host', default=config['host'])
engine = create_engine('mysql://{}:{}@{}'.format(root_u, root_p, host))
conn = engine.connect()

# Create the database and user.
dbname = user_input('Database', default=config['db_name'])
user1 = user_input('Username', default=config['username'])
pass1 = user_input('Password', default=config['password'])
try:
    conn.execute('CREATE DATABASE {}'.format(dbname))
    conn.execute('CREATE USER "{}"@"{}" IDENTIFIED BY "{}"'.format(
            user1, host, pass1))
    conn.execute('GRANT ALL ON `{}`.* TO "{}"@"{}"'.format(
            dbname, user1, host))
except: 
    print('Failed to create.')

# Disconnect from database engine.
conn.close()
