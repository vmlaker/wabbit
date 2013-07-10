"""Record video frames to disk, and mark the timestamps in database."""

import datetime as dt
import os
import sys
import cv2
import sqlalchemy as sa
import mpipe
import coils
import mapping

# Read command-line parameters.
DEVICE = int(sys.argv[1])
WIDTH = int(sys.argv[2])
HEIGHT = int(sys.argv[3])
DURATION = float(sys.argv[4])
CONFIG = sys.argv[5] if len(sys.argv)>=6 else 'wabbit.cfg'

# Create the OpenCV video capture object.
cap = cv2.VideoCapture(DEVICE)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# Load configuration file.
config = coils.Config(CONFIG)

# Monitor framerates for past few seconds.
ticker = coils.RateTicker((1, 2, 5))

def save2disk((tstamp, image)):

    # Create destination directory.
    dname = coils.time2dir(tstamp)
    dname = os.path.join(config['pics_dir'], dname)
    try: 
        os.makedirs(dname)
    except OSError:
        pass

    # Save the file.
    fname = os.path.join(dname, coils.time2fname(tstamp)) + '.png'
    cv2.imwrite(fname, image)
    return tstamp

class DbWriter(mpipe.UnorderedWorker):
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
        image = mapping.Image(dt.datetime.now())
        self._sess.add(image)

        # Increment the size.
        self._sess.query(mapping.Datum).\
            filter(mapping.Datum.name=='size').\
            update({'value':mapping.Datum.value+1})

        # Update latest timestamp.
        self._sess.query(mapping.Datum).\
            filter(mapping.Datum.name=='last_tstamp').\
            update({'value': coils.time2string(tstamp)})

        # Commit the transaction.
        self._sess.commit()


stage1 = mpipe.UnorderedStage(save2disk, 8)
stage2 = mpipe.Stage(DbWriter, 8)
pipe1 = mpipe.Pipeline(stage1.link(stage2))

# Go into main loop.
end = dt.datetime.now() + dt.timedelta(seconds=DURATION)
while end > dt.datetime.now():

    # Take a snapshot, mark the timestamp and put on pipeline.
    hello, image = cap.read()
    now = dt.datetime.now()
    pipe1.put((now, image))

    # Display the image.
    #cv2.namedWindow('wabbit', cv2.cv.CV_WINDOW_NORMAL)
    #cv2.imshow('wabbit', image)
    #cv2.waitKey(1)

    print('{}, {}, {}'.format(*ticker.tick()))

# Stop the pipeline.
pipe1.put(None)
