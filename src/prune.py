"""Prune database and disk of old images.

Parameters:  <older_than_sec> [<config_file>]

Disk is pruned to the next 60 s boundary. 
To prune all files use seconds value <= -60.
"""

import datetime as dt
import os
import sys
import shutil
import logging

import sqlalchemy as sa
import coils
import mapping
from log_format import getFormat

# Read command-line parameters.
SECONDS = float(sys.argv[1])
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

# Connect to database engine and start a session.
engine = sa.create_engine(
    'mysql://{}:{}@{}/{}'.format(
        config['username'], config['password'], 
        config['host'], config['db_name']))
try:
    conn = engine.connect()
except sa.exc.OperationalError:
    logging.error('Failed to connect.')
    sys.exit(1)

# Compute the oldest timestamp allowed.
now = dt.datetime.now()
delta = dt.timedelta(seconds=SECONDS)
then = now - delta
logger.debug('Removing older than {}s ==> {}'.format(SECONDS, then))


# Update the database.
# First remove rows from the image table,
# and then update size entry in the info table.
Session = sa.orm.sessionmaker(bind=engine)
session = Session()
timer = coils.Timer()
try:

    # Remove the images.
    count = session.query(mapping.Image).filter(mapping.Image.time < then).delete()
    logger.info('Deleted {} rows.'.format(count))

    # Decrement the size.
    session.query(mapping.Datum).\
        filter(mapping.Datum.name=='size').\
        update({'value':mapping.Datum.value-count})

except sa.exc.OperationalError, ee:

    logger.error('Failed to delete records.')
    logger.error('Exception: {}'.format(str(ee)))

logger.debug('Elapsed {}'.format(timer.get().total_seconds()))
session.commit()


# Define an error handler for deletion of entire directory tree.
def on_rmtree_error(func, path, excinfo):
    """Error handler for shutil.rmtree -- simply log the error details."""
    logger.error('rmtree error: func    {}'.format(str(func)))
    logger.error('              path    {}'.format(path))
    logger.error('              excinfo {}'.format(excinfo))
    
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
            shutil.rmtree(full, ignore_errors=False, onerror=on_rmtree_error)
            logger.info('Removed {}'.format(full))

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
        logger.info('Removed {}'.format(full))
        
os.chdir(saved)  # Popd.
