"""Record video frames to disk, and mark the timestamps in database.
Parameters:  <duration_sec> [<config_file>]
"""

# Import standard modules.
import datetime as dt
import os
import sys
import time

# Import 3rd party modules.
import cv2
import sqlalchemy as sa
import mpipe
import coils

# Import local modules.
import mapping

# Read command-line parameters.
DURATION = float(sys.argv[1])
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.cfg'

# Load configuration file.
config = coils.Config(CONFIG)

def save2disk((tstamp, image)):
    """First stage of the pipeline;
    saves the image to disk."""

    # Create destination directory.
    dname = coils.time2dir(tstamp)
    dname = os.path.join(config['pics_dir'], dname)
    try: 
        os.makedirs(dname)
    except OSError:
        pass

    # Save the file.
    fname = os.path.join(dname, coils.time2fname(tstamp)) + '.' + config['f_ext']
    cv2.imwrite(fname, image)
    return tstamp

class DbWriter(mpipe.UnorderedWorker):
    """Second stage of the pipeline; 
    updates the SQL database."""

    def __init__(self):
        """Connect to database engine and start a session."""
        engine = sa.create_engine(
            'mysql://{}:{}@{}/{}'.format(
                config['username'], config['password'], 
                config['host'], config['db_name']))
        Session = sa.orm.sessionmaker(bind=engine)
        self._sess = Session()

    def doTask(self, tstamp):
        """Write to the database."""

        # Add the item.
        image = mapping.Image(tstamp)
        self._sess.add(image)

        # Increment the size.
        self._sess.query(mapping.Datum).\
            filter(mapping.Datum.name=='size').\
            update({'value':mapping.Datum.value+1})

        # Update latest timestamp.
        self._sess.query(mapping.Datum).\
            filter(mapping.Datum.name=='latest_tstamp').\
            update({'value': coils.time2string(tstamp)})

        # Commit the transaction.
        self._sess.commit()

# Create the OpenCV video capture object.
cap = cv2.VideoCapture(int(config['device']))
if not cap.isOpened():
    print('Cannot open device {}.'.format(int(config['device'])))
    sys.exit(1)
cap.set(3, int(config['width']))
cap.set(4, int(config['height']))

# Create the image post-processing pipeline.
stage1 = mpipe.UnorderedStage(save2disk, 8)
stage2 = mpipe.Stage(DbWriter, 8)
pipe1 = mpipe.Pipeline(stage1.link(stage2))

# Monitor framerates for past few seconds.
ticker = coils.RateTicker((2, 5, 10))

# Go into main loop.
prev = dt.datetime.now()  # Keep track of previous snapshot time.
min_interval = 1/float(config['max_fps'])
end = dt.datetime.now() + dt.timedelta(seconds=abs(DURATION))
while end > dt.datetime.now() or DURATION < 0:

    # Insert delay to observe maximum framerate limit.
    elapsed = (dt.datetime.now() - prev).total_seconds()
    sleep_time = min_interval - elapsed
    sleep_time = max(0, sleep_time)
    time.sleep(sleep_time)
    prev = dt.datetime.now()

    # Take a snapshot, and bail out of loop if the snapshot failed.
    # The only way I could detect camera disconnect was by
    # thresholding the length of time to call read() method;
    # for some reason return value of read() is always True, 
    # even after disconnecting the camera.
    timer = coils.Timer()
    retval, image = cap.read()

    # When timing the read() call, set min_read 
    # config value to 0. Then trip the timer (and print
    # the value) by uncommenting the line below.
    #print(timer.get())  

    if not retval or timer.get().total_seconds() < float(config['min_read']):
        print('Failed to read from camera.')
        break  # Bail out.

    # Put image on the pipeline.
    pipe1.put((prev, image))

    # Display the image.
    #cv2.namedWindow('wabbit', cv2.cv.CV_WINDOW_NORMAL)
    #cv2.imshow('wabbit', image)
    #cv2.waitKey(1)

    print('{:.2f}, {:.2f}, {:.2f}'.format(*ticker.tick()))

# Stop the pipeline.
pipe1.put(None)
