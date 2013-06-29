"""Drop MySQL user and database."""

import sys
import sqlalchemy as sa
import coils

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Connect to database engine.
root_u = coils.user_input('Admin username', default=config['admin'])
root_p = coils.user_input('Admin password', password=True)
engine = sa.create_engine(
        'mysql://{}:{}@{}'.format(root_u, root_p, config['host']))
conn = engine.connect()

# Drop the user and database.
try:
    conn.execute('REVOKE ALL PRIVILEGES, GRANT OPTION FROM "{}"@"{}"'.format(
            config['username'], config['host']))
    conn.execute('DROP USER "{}"@"{}"'.format(
            config['username'], config['host']))
except:
    print('Failed to drop user.')
try:
    conn.execute('DROP DATABASE {}'.format(config['db_name']))
except:
    print('Failed to drop database.')

# Disconnect from database engine.
conn.close()
