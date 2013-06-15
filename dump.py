"""Dump the database."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from coils import user_input, Config

config = Config('wabbit.cfg')

# Connect to database engine and start a session.
dbname = user_input('Database', default=config['db_name'])
user1 = user_input('Username', default=config['username'])
pass1 = user_input('Password', default=config['password'])
host = user_input('Host', default=config['host'])
engine = create_engine('mysql://{}:{}@{}/{}'.format(user1, pass1, host, dbname))
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

# Dump the table.
from Image import Image
for instance in session.query(Image).order_by(Image.id):
     print(instance)

# Close the session.
conn.close()
