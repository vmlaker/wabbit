"""Dump all images."""

import sys
import sqlalchemy as sa
import coils
import mapping

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Connect to database engine and start a session.
engine = sa.create_engine(
     'mysql://{}:{}@{}/{}'.format(
          config['username'], config['password'],
          config['host'], config['db_name']))
try:
    conn = engine.connect()
except sa.exc.OperationalError:
    print('Failed to connect.')
    sys.exit(1)

Session = sa.orm.sessionmaker(bind=engine)
session = Session()
for image in session.query(mapping.Image):
     print(image)
