"""Add a timestamp."""

from coils import user_input, Config
from sqlalchemy import create_engine, Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = Config('wabbit.cfg')

# Connect to database engine and start a session.
dbname = user_input('Database name', default=config['db_name'])
user1 = user_input('Username', default=config['username'])
pass1 = user_input('Password', default=config['password'])
host = user_input('Host', default=config['host'])
engine = create_engine('mysql://{:}:{:}@{:}/{:}'.format(user1, pass1, host, dbname))
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

# Declare a mapping.
Base = declarative_base()
class Image(Base):
     __tablename__ = 'images'

     id = Column(Integer, primary_key=True)
     tstamp = Column(DateTime())

     def __init__(self, tstamp):
         self.tstamp = tstamp

     def __repr__(self):
        return "<Image('{:}')>".format(self.tstamp)

# Create the table.
Base.metadata.create_all(engine)

# Create the object.
import datetime
image1 = Image(datetime.datetime.now())

# Persist the object.
session.add(image1)

# Commit the transaction.
session.commit()

# Close the session.
conn.close()
