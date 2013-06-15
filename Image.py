"""Image mapping."""
from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from coils import time2string


# Declare the mapping.
Base = declarative_base()
class Image(Base):
     __tablename__ = 'images'
     
     id = Column(Integer, primary_key=True)
     tstamp = Column(String(len(time2string(datetime.now()))))
     
     def __init__(self, tstamp):
          self.tstamp = time2string(tstamp)
          
     def __repr__(self):
          return "<Image('{}')>".format(self.tstamp)
