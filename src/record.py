"""Record video frames to disk, and mark the timestamps in database.

Parameters:  <duration_sec> [<config_file>]
"""

# Import standard modules.
import datetime as dt
import os
import sys
import time
import logging

# Import 3rd party modules.
import cv2
import mpipe
import coils

# Import local modules.
from mpipe_stages import DiskSaver, DbWriter
from log_format import getFormat

# Read command-line parameters.
DURATION = float(sys.argv[1])
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.cfg'

# Configure logging and get the logger object.
logging.basicConfig(
    stream=sys.stdout,
    format=getFormat(),
    level=logging.DEBUG,
    )
logger = logging.getLogger('prune')

# Load configuration file.
config = coils.Config(CONFIG)

# Create the OpenCV video capture object.
cap = cv2.VideoCapture(int(config['device']))
if not cap.isOpened():
    logger.error('Cannot open device {}.'.format(int(config['device'])))
    sys.exit(1)
logger.info('Opened device {}.'.format(int(config['device'])))
cap.set(3, int(config['width']))
cap.set(4, int(config['height']))

# Create the image post-processing pipeline.
pipe1 = mpipe.Pipeline(
    mpipe.Stage(DiskSaver, 8, config=config).link(
        mpipe.Stage(DbWriter, 8, config=config)))

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

    # When timing the read() call, set min_read config value to 0. 
    # Then trip the timer (and dump the value) by uncommenting the line below.
    #logger.debug(timer.get())  

    if not retval or timer.get().total_seconds() < float(config['min_read']):
        logger.error('Failed to read from camera.')
        break  # Bail out.

    # Put image on the pipeline.
    pipe1.put((prev, image))

    # Display the image.
    #cv2.namedWindow('wabbit', cv2.cv.CV_WINDOW_NORMAL)
    #cv2.imshow('wabbit', image)
    #cv2.waitKey(1)

    logger.debug('{:.2f}, {:.2f}, {:.2f}'.format(*ticker.tick()))

# Stop the pipeline.
pipe1.put(None)
