import datetime as dt
import sqlalchemy as sa
import coils

metadata = sa.MetaData()
image = sa.Table(
     'image', metadata,
     sa.Column(
          'tstamp', 
          sa.String(len(coils.time2string(dt.datetime.now()))),
          primary_key=True),
     )
