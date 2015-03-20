"""Create a movie.

Parameters:  <begin_time> <length_sec> <config_file> [<speedup>]
"""

import sys
import datetime as dt

import mpipe
import sqlalchemy as sa
import sqlalchemy.orm as orm 

import coils
import mapping
from mpipe_stages import DiskReader, Viewer


# Read command-line parameters.
BEGIN = sys.argv[1]
LENGTH = int(sys.argv[2])
CONFIG = sys.argv[3]
SPEEDUP = float(sys.argv[4]) if len(sys.argv)>=5 else 1.0

# Load configuration file.
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

# Assemble the pipeline.
pipe = mpipe.Pipeline(
    mpipe.Stage(DiskReader, 8, config=config).link(
        mpipe.Stage(Viewer, speedup=SPEEDUP)))

# Compute the end time.
delta = dt.timedelta(seconds=LENGTH)
begin = coils.string2time(BEGIN)
end = begin + delta if LENGTH > 0 else dt.datetime.now()

# Retrieve image timestamps.
images = session.query(mapping.Image.time).\
    filter(mapping.Image.time > begin).\
    filter(mapping.Image.time < end).\
    group_by(mapping.Image.time).all()
times = [ii[0] for ii in images]
print('Playing {} images.'.format(len(times)))

# Process timestamps in the pipeline.
for time in times:
    pipe.put(time)

# Stop the pipeline.
pipe.put(None)
