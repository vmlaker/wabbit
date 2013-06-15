"""Add a timestamp."""

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

# Create the object.
import datetime
from Image import Image, Base
Base.metadata.create_all(engine)
image1 = Image(datetime.datetime.now())

# Persist the object.
session.add(image1)

# Commit the transaction.
session.commit()

# Close the session.
conn.close()
