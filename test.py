from coils import user_input
from sqlalchemy import create_engine

username = user_input('Username', default='root')
password = user_input('Password', password=True)
dbname = user_input('Database name')

engine = create_engine(
    'mysql://{:}:{:}@localhost'.format(username, password),
    isolation_level='READ UNCOMMITTED'
    )
conn = engine.connect()
conn.execute('drop database {:}'.format(dbname))
conn.close()
