"""Prune database and disk of old images.
Arguments:  seconds [cfg_file]
  seconds   -  minimum age of removed items
  cfg_file  -  config file
Disk is pruned to the next 60 s boundary. 
To prune all files use seconds value <= -60.
"""

import datetime as dt
import os
import sys
import shutil
import sqlalchemy as sa
import coils
import tables

# Read command-line parameters.
SECONDS = float(sys.argv[1])
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.cfg'

# Load configuration file.
config = coils.Config(CONFIG)

# Connect to database engine and start a session.
engine = sa.create_engine(
    'mysql://{}:{}@{}/{}'.format(
        config['username'], config['password'], 
        config['host'], config['db_name']))
conn = engine.connect()

# Compute the oldest timestamp allowed.
now = dt.datetime.now()
delta = dt.timedelta(seconds=SECONDS)
then = now - delta

# Remove from database.
rem = tables.image.delete().where(tables.image.c.tstamp < then)
result = conn.execute(rem)
print('Deleted {} rows.'.format(result.rowcount))

# Remove from disk.
levels = coils.time2levels(then)
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
            shutil.rmtree(full, ignore_errors=True)
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
