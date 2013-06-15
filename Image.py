"""Image mapping."""
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

# Declare the mapping.
Base = declarative_base()
class Image(Base):
     __tablename__ = 'images'
     
     id = Column(Integer, primary_key=True)
     tstamp = Column(DateTime())
     
     def __init__(self, tstamp):
          self.tstamp = tstamp
          
     def __repr__(self):
          return "<Image('{}')>".format(self.tstamp)
