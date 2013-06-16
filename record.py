"""Record video frames to disk, and mark the timestamps in database."""

from datetime import datetime, timedelta
import os
import sys
import cv2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coils import time2fname, time2dir, user_input, Config, RateTicker
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
title = 'playing OpenCV capture'
cv2.namedWindow(title, cv2.cv.CV_WINDOW_NORMAL)

# Load configuration file.
config = Config('wabbit.cfg')

# Connect to database engine and start a session.
dbname = user_input('Database', default=config['db_name'])
user1 = user_input('Username', default=config['username'])
pass1 = user_input('Password', default=config['password'])
host = user_input('Host', default=config['host'])
engine = create_engine('mysql://{}:{}@{}/{}'.format(user1, pass1, host, dbname))
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

# Monitor framerates for past few seconds.
ticker = RateTicker((1, 2, 5))

# Go into main loop.
end = datetime.now() + timedelta(seconds=DURATION)
while end > datetime.now():

    print('{}, {}, {}'.format(*ticker.tick()))

    # Take a snapshot and mark the timestamp.
    hello, image = cap.read()
    now = datetime.now()

    # Create destination directory.
    dname = time2dir(now)
    if not os.path.isdir(dname):
        os.makedirs(dname)

    # Save the file.
    fname = os.path.join(dname, time2fname(now)) + '.png'
    cv2.imwrite(fname, image)

    # Create the object.
    Base.metadata.create_all(engine)
    image1 = Image(now)

    # Persist the object.
    session.add(image1)

    # Commit the transaction.
    session.commit()

    # Display the image.
    cv2.imshow(title, image)
    cv2.waitKey(1)

# Close the session.
conn.close()




