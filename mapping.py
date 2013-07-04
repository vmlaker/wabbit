"""ORM mappings using SQLAlchemy."""

import datetime as dt
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import coils

# Create the base class.
Base = declarative_base()


class Image(Base):
    """Mapping for "images" table."""

    __tablename__ = 'images'
    id = sa.Column(sa.Integer, primary_key=True)
    time = sa.Column(sa.String(
            len(coils.time2string(dt.datetime.now()))))

    def __init__(self, tstamp):
        self.time = coils.time2string(tstamp)

    def __repr__(self):
        return '<Image("{}")>'.format(self.time)


class Datum(Base):
    """Mapping for "info" table."""

    __tablename__ = 'info'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64))
    value = sa.Column(sa.String(64))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<Datum("{} {}")>'.format(self.name, self.value)
