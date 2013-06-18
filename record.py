"""Record video frames to disk, and mark the timestamps in database."""

from datetime import datetime, timedelta
import os
import sys
import cv2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import coils
from Image import Image, Base

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

# Connect to database engine and start a session.
engine = create_engine(
    'mysql://{}:{}@{}/{}'.format(
        config['username'], config['password'], 
        config['host'], config['db_name']))
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

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

def write2db(tstamp):

    # Create the object.
    Base.metadata.create_all(engine)
    image1 = Image(tstamp)

    # Persist the object.
    session.add(image1)

    # Commit the transaction.
    session.commit()

from mpipe import Pipeline, UnorderedStage as UStage
stage1 = UStage(save2disk, 3)
stage2 = UStage(write2db, 3)
pipe1 = Pipeline(stage1.link(stage2))

# Go into main loop.
end = datetime.now() + timedelta(seconds=DURATION)
while end > datetime.now():

    # Take a snapshot and mark the timestamp.
    hello, image = cap.read()
    now = datetime.now()

    pipe1.put((now, image))

    # Display the image.
    #cv2.namedWindow('wabbit', cv2.cv.CV_WINDOW_NORMAL)
    #cv2.imshow('wabbit', image)
    #cv2.waitKey(1)

    print('{}, {}, {}'.format(*ticker.tick()))

# Close the session and stop the pipeline.
conn.close()
pipe1.put(None)
