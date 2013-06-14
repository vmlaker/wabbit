from getpass import getpass
from sqlalchemy import create_engine

username = raw_input('Username: ')
password = getpass('Password: ')
dbname = raw_input('Database name: ')

engine = create_engine(
    'mysql://{:}:{:}@localhost'.format(username, password),
    isolation_level='READ UNCOMMITTED'
    )
conn = engine.connect()
conn.execute('drop database {:}'.format(dbname))
conn.close()
