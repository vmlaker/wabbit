"""Drop MySQL user and database, as configured in wabbit.cfg file."""

from coils import user_input, Config
from sqlalchemy import create_engine

config = Config('wabbit.cfg')

# Connect to database engine.
root_u = user_input('Admin username', default=config['admin'])
root_p = user_input('Admin password', password=True)
engine = create_engine(
        'mysql://{}:{}@{}'.format(root_u, root_p, config['host']))
conn = engine.connect()

# Drop the user and database.
try:
    conn.execute('REVOKE ALL PRIVILEGES, GRANT OPTION FROM "{}"@"{}"'.format(
            config['username'], config['host']))
    conn.execute('DROP USER "{}"@"{}"'.format(
            config['username'], config['host']))
    conn.execute('DROP DATABASE {}'.format(config['db_name']))
except:
    print('Failed to drop.')

# Disconnect from database engine.
conn.close()
