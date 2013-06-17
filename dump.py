"""Dump the database."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from coils import user_input, Config

config = Config('wabbit.cfg')

# Connect to database engine and start a session.
engine = create_engine(
     'mysql://{}:{}@{}/{}'.format(
          config['username'], config['password'],
          config['host'], config['db_name']))
conn = engine.connect()
session = sessionmaker(bind=engine)()

# Dump the table.
from Image import Image
for instance in session.query(Image).order_by(Image.id):
     print(instance)

# Close the session.
conn.close()
