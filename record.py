"""Record video frames to disk, and mark the timestamps in database."""

from datetime import datetime, timedelta
import os
import sys
import cv2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import coils
from Image import Image, Base

DEVICE = int(sys.argv[1])
WIDTH = int(sys.argv[2])
HEIGHT = int(sys.argv[3])
DURATION = float(sys.argv[4])

# Create the OpenCV video capture object.
cap = cv2.VideoCapture(DEVICE)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# Create the display window.
title = 'wabbit'
cv2.namedWindow(title, cv2.cv.CV_WINDOW_NORMAL)

# Load configuration file.
config = coils.Config('wabbit.cfg')

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

# Go into main loop.
end = datetime.now() + timedelta(seconds=DURATION)
while end > datetime.now():

    # Take a snapshot and mark the timestamp.
    hello, image = cap.read()
    now = datetime.now()

    # Create destination directory.
    dname = coils.time2dir(now)
    dname = os.path.join(config['pics_dir'], dname)
    if not os.path.isdir(dname):
        os.makedirs(dname)

    # Save the file.
    timer = coils.Timer()
    fname = os.path.join(dname, coils.time2fname(now)) + '.png'
    cv2.imwrite(fname, image)
    t1 = timer.get().total_seconds()

    # Create the object.
    Base.metadata.create_all(engine)
    image1 = Image(now)

    # Persist the object.
    session.add(image1)

    # Commit the transaction.
    session.commit()
    t2 = timer.get().total_seconds()

    # Display the image.
    cv2.imshow(title, image)
    cv2.waitKey(1)

    print('{}, {}, {}  {:.3f}  {:.3f}'.format(
            *ticker.tick() + (t1, t2)))

# Close the session.
conn.close()



