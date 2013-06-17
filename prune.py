"""Prune database and disk of old images."""

from datetime import datetime, timedelta
import os
import sys
import shutil
import cv2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from coils import Config, string2time, time2fname, time2levels

SECONDS = float(sys.argv[1])

# Load configuration file.
config = Config('wabbit.cfg')

# Connect to database engine and start a session.
engine = create_engine(
    'mysql://{}:{}@{}/{}'.format(
        config['username'], config['password'], 
        config['host'], config['db_name']))
conn = engine.connect()
session = sessionmaker(bind=engine)()

# Compute the oldest timestamp allowed.
now = datetime.now()
delta = timedelta(seconds=SECONDS)
then = now - delta

# Remove from database.
from Image import Image, Base
Base.metadata.create_all(engine)
session.query(Image).filter(Image.tstamp<then).delete()
session.commit()

# Delete from disk.
levels = time2levels(then)
saved = os.getcwd()
os.chdir(config['pics_dir'])
for level in levels:
    
    for entry in os.listdir('.'):
        try:
            int_entry = int(entry)
        except:
            continue
        if int_entry < int(level):
            full = os.path.join(os.getcwd(), entry)
            print('Erasing {}'.format(full))
            shutil.rmtree(full)

    # Skip if not a directory.
    if not os.path.isdir(level):
        break
    os.chdir(level)

os.chdir(saved)

