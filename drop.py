"""Drop MySQL user and database, as configured in wabbit.cfg file."""

from coils import user_input, Config
from sqlalchemy import create_engine

config = Config('wabbit.cfg')

# Connect to database engine.
root_u = user_input('Admin username', default=config['admin'])
root_p = user_input('Admin password', password=True)
host = user_input('Host', default=config['host'])
engine = create_engine('mysql://{}:{}@{}'.format(root_u, root_p, host))
conn = engine.connect()

# Drop the user and database.
dbname = user_input('Database', default=config['db_name'])
user1 = user_input('Username', default=config['username'])
pass1 = user_input('Password', default=config['password'])
try:
    conn.execute('REVOKE ALL PRIVILEGES, GRANT OPTION FROM "{}"@"{}"'.format(
            user1, host))
    conn.execute('DROP USER "{}"@"{}"'.format(
            user1, host))
    conn.execute('DROP DATABASE {}'.format(dbname))
except:
    print('Failed to drop.')

# Disconnect from database engine.
conn.close()
