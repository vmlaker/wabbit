"""Pruner class."""

import datetime
import logging
import os
import sys
import shutil
import time

import sqlalchemy as sa
import coils
import mapping
from log_format import getFormat

class Pruner:
    
    def __init__(self, config):

        self.config = config
        
        # Configure logging and get the logger object.
        logging.basicConfig(
            stream=sys.stdout,
            format=getFormat(),
            level=logging.DEBUG,
        )
        self.logger = logging.getLogger('prune')
        
        # Connect to database engine and start a session.
        self.engine = sa.create_engine(
            'mysql://{}:{}@{}/{}'.format(
                self.config['username'], self.config['password'], 
                self.config['host'], self.config['db_name']))
        try:
            conn = self.engine.connect()
        except sa.exc.OperationalError:
            self.logger.error('Failed to connect.')
            sys.exit(1)

    def run(self):
        """Prune forever."""
        sleep_time = float(self.config['prune_sleep'])
        while True:
            self.prune()
            self.logger.debug('Sleeping {}s...'.format(sleep_time))
            time.sleep(sleep_time)
        
    def prune(self):
        """Prune the database and filesystem."""
        
        # Compute the oldest timestamp allowed.
        max_history = float(self.config['max_history'])
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=max_history)
        oldest = now - delta

        self.logger.debug('Removing older than {}s (i.e. {})'.format(max_history, oldest))
        self.logger.debug('Pruning database...')
        timer = coils.Timer()
        count = self.prune_db(oldest)
        self.logger.debug('Elapsed {}, deleted {} rows'.format(timer.get().total_seconds(), count))
        self.logger.debug('Pruning filesystem...')
        self.prune_fs(oldest)
        self.logger.debug('Elapsed {}'.format(timer.get().total_seconds()))

        
    def prune_db(self, oldest):
        """
        Prune the database, given timestamp 
        of the oldest allowed entry.
        Return number of rows deleted.
        """
        
        # First remove rows from the image table,
        # and then update size entry in the info table.
        Session = sa.orm.sessionmaker(bind=self.engine)
        session = Session()
        count = 0  # Keep a count of number of rows deleted.
        try:
             # Remove the image entries.
            count = session.query(mapping.Image).filter(mapping.Image.time < oldest).delete()

            # Decrement the size.
            session.query(mapping.Datum).\
                filter(mapping.Datum.name=='size').\
                update({'value':mapping.Datum.value-count})

        except sa.exc.OperationalError, ee:

            self.logger.error('Failed to delete records.')
            self.logger.error('Exception: {}'.format(str(ee)))

        session.commit()
        return count

    
    def prune_fs(self, oldest):
        """
        Prune the filesystem, given timestamp 
        of the oldest allowed entry.
        """
        
        # Define an error handler for deletion of entire directory tree.
        def on_rmtree_error(func, path, excinfo):
            """Error handler for shutil.rmtree -- simply log the error details."""
            self.logger.error('rmtree error: func    {}'.format(str(func)))
            self.logger.error('              path    {}'.format(path))
            self.logger.error('              excinfo {}'.format(excinfo))
    
        # Remove from disk.
        levels = coils.time2levels(oldest)
        dstack = list()  # Stack of descended subdirectories.
        saved = os.getcwd()  # Pushd.

        # Start at the root level, i.e. the top of 
        # the pics directory (where the years are listed).
        os.chdir(self.config['pics_dir'])

        # For each level (Y, M, D, h, m) starting with the year,
        # prune the archive file structure of all older directories,
        # while descending into the archive.
        for level in levels:
    
            # Compare every directory with the current level, and
            # if the directory is older than the level 
            # (it's name being a smaller number) erase it.
            for entry in os.listdir('.'):

                # Skip if entry is not a numeric integer string.
                try:
                    int_entry = int(entry)
                except:
                    continue
                
                # Only interested in entries less than the level
                # (i.e. older than the level) so skip the others.
                if int_entry >= int(level):
                    continue

                # Remove the filesystem path.
                full = os.path.join(os.getcwd(), entry)
                shutil.rmtree(full, ignore_errors=False, onerror=on_rmtree_error)
                self.logger.info('Removed {}'.format(full))

            # Now that we've removed the current level's older
            # directories, descend into the next level.

            # If we can't find the directory for the current label,
            # then we're done.
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
                self.logger.info('Removed {}'.format(full))
        
        os.chdir(saved)  # Popd.


if __name__ == '__main__':

    usage = 'Usage:  python prune.py [<config_file>]'

    try:
        CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.conf'
    except:
        print(usage)
        sys.exit(1)

    # Load configuration file.
    config = coils.Config(CONFIG)

    pruner = Pruner(config)
    pruner.run()
    
