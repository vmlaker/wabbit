"""Prune database and disk of old images.
Arguments:  seconds [cfg_file]
  seconds   -  minimum age of removed items
  cfg_file  -  config file
Disk is pruned to the next 60 s boundary. 
To prune all files use seconds value <= -60.
"""

from datetime import datetime, timedelta
import os
import sys
import shutil

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from coils import Config, time2levels

# Read command-line parameters.
SECONDS = float(sys.argv[1])
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.cfg'

# Load configuration file.
config = Config(CONFIG)

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
count = session.query(Image).filter(Image.tstamp<then).delete()
session.commit()
if count:
    print('Deleted {} rows.'.format(count))

# Remove from disk.
levels = time2levels(then)
dstack = list()  # Stack of descended subdirectories.
saved = os.getcwd()  # Pushd.
os.chdir(config['pics_dir'])
for level in levels:
    
    for entry in os.listdir('.'):
        try:
            int_entry = int(entry)
        except:
            continue
        if int_entry < int(level):
            full = os.path.join(os.getcwd(), entry)
            shutil.rmtree(full)
            print('Removed {}'.format(full))

    # Skip if not a directory.
    if not os.path.isdir(level):
        break

    # Descend into subdirectory.
    os.chdir(level)  
    dstack.append(level)

# Delete empty subdirectories. 
for entry in reversed(dstack):
    if not os.listdir('.'):
        os.chdir('..')
        full = os.path.join(os.getcwd(), entry)
        shutil.rmtree(full)
        print('Removed {}'.format(full))
        
os.chdir(saved)  # Popd.
