"""Dump the database."""

import sys
import sqlalchemy as sa
import coils
import tables

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Connect to database engine and start a session.
engine = sa.create_engine(
     'mysql://{}:{}@{}/{}'.format(
          config['username'], config['password'],
          config['host'], config['db_name']))
conn = engine.connect()

# Select and print.
s = sa.sql.select([tables.image])
result = conn.execute(s)
for row in result:
     print(row)
