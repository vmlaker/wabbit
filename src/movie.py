"""Create a movie.
Parameters:  <begin_time> <length_sec> <speedup> [<config> | <url> <dir>]
"""

import os
import sys
import time
import datetime as dt
import urllib
import urllib2
import simplejson as json
import sqlalchemy as sa
import sqlalchemy.orm as orm 

import cv2
import mpipe

import coils
import mapping

# Read command-line parameters.
BEGIN = sys.argv[1]
LENGTH = int(sys.argv[2])
SPEEDUP = float(sys.argv[3])
CONFIG = sys.argv[4] if len(sys.argv) == 5 else 'wabbit.cfg'
URL = sys.argv[4] if len(sys.argv) >= 6 else None
PICS_DIR = sys.argv[5] if len(sys.argv) >= 6 else None

# Load configuration file.
config = coils.Config(CONFIG)

def read(tstamp):
    """Read image from disk and propagate it downstream."""
    tstamp = coils.string2time(tstamp)
    fname = coils.time2fname(tstamp, full=True) + '.' + config['f_ext']
    pics_dir = PICS_DIR if PICS_DIR else config['pics_dir']
    fname = os.path.join(pics_dir, fname)
    image = cv2.imread(fname)
    return tstamp, image

cv2.namedWindow('wabbit', cv2.cv.CV_WINDOW_NORMAL)
class Viewer(mpipe.OrderedWorker):
    """Displays image in a window."""

    def __init__(self):
        self._prev_tstamp = dt.datetime.max
        self._prev_dotask = dt.datetime.max

    def doTask(self, (tstamp, image)):

        # Compute time difference between timestamps.
        diff_tstamp = tstamp - self._prev_tstamp
        self._prev_tstamp = tstamp
        diff_tstamp = diff_tstamp.total_seconds()
        diff_tstamp = max(0, diff_tstamp)
        diff_tstamp /= SPEEDUP

        # Compute time elapsed since previous doTask().
        elapsed = dt.datetime.now() - self._prev_dotask
        elapsed = elapsed.total_seconds()
        elapsed = max(0, elapsed)
        
        # Pause to match real framerate.
        sleep_time = diff_tstamp - elapsed
        if sleep_time < 0:
            self._prev_dotask = dt.datetime.now()
            return
        time.sleep(sleep_time)
        self._prev_dotask = dt.datetime.now()

        try:
            cv2.imshow('wabbit', image)
            cv2.waitKey(1)
        except:
            print('Error in viewer !!!')

# Assemble the pipeline.
s1 = mpipe.OrderedStage(read,8)
s2 = mpipe.Stage(Viewer)
pipe = mpipe.Pipeline(s1.link(s2))

if URL:
    # Retrieve timestamps from server.
    args = { 'begin' : BEGIN, 'length' : LENGTH }
    data = urllib.urlencode(args)
    url = '{}/service/tstamps?{}'.format(URL, data)
    response = urllib.urlopen(url)
    result = json.loads(response.read())
    times = result['images']

    print('Playing {} images.'.format(len(times)))
    for time in times:
        pipe.put(time)
    pipe.put(None)
    sys.exit(0)

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
