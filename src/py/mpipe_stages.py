"""Various MPipe stages."""

import os
import time
import datetime as dt

import cv2
import sqlalchemy as sa
import wget
import mpipe

import coils
import mapping


class DiskReader(mpipe.OrderedWorker):
    """Reads image from disk."""

    def __init__(self, config):
        """Initialize the object."""
        self._config = config

    def doTask(self, tstamp):
        """Read image from disk and propagate it downstream."""
        tstamp = coils.string2time(tstamp)
        fname = coils.time2fname(tstamp, full=True) + '.jpg'
        fname = os.path.join(self._config['pics_dir'], fname)
        image = cv2.imread(fname)
        return tstamp, image


class DiskSaver(mpipe.UnorderedWorker):
    """Saves image to disk."""

    def __init__(self, config):
        """Initialize the object."""
        self._config = config

    def doTask(self, (tstamp, image)):
        """Save image to disk."""

        # Create destination directory.
        dname = coils.time2dir(tstamp)
        dname = os.path.join(self._config['pics_dir'], dname)
        try: 
            os.makedirs(dname)
        except OSError:
            pass

        # Save the file.
        fname = os.path.join(dname, coils.time2fname(tstamp)) + '.jpg'
        cv2.imwrite(fname, image)

        # Propagate timestamp downstream.
        return tstamp


class DbWriter(mpipe.UnorderedWorker):
    """Writes data to MySQL database."""

    def __init__(self, config):
        """Initialize the object.
        Connect to database engine and start a session."""
        self._config = config
        engine = sa.create_engine(
            'mysql://{}:{}@{}/{}'.format(
                self._config['username'], self._config['password'], 
                self._config['host'], self._config['db_name']))

        # Raises exception upon failed connect.
        engine.connect()  

        Session = sa.orm.sessionmaker(bind=engine)
        self._sess = Session()

    def doTask(self, tstamp):
        """Write to the database."""

        # Add the item.
        image = mapping.Image(tstamp)
        self._sess.add(image)

        # Increment the size.
        self._sess.query(mapping.Datum).\
            filter(mapping.Datum.name=='size').\
            update({'value':mapping.Datum.value+1})

        # Update latest timestamp.
        self._sess.query(mapping.Datum).\
            filter(mapping.Datum.name=='latest_tstamp').\
            update({'value': coils.time2string(tstamp)})

        # Commit the transaction.
        self._sess.commit()


class Downloader(mpipe.UnorderedWorker):
    """Downloads file associated with given timestamp."""

    def __init__(self, config, url):
        """Initilize the object."""
        self._config = config
        self._url = url

    def doTask(self, tstamp):
        """Download image."""
        tstamp = coils.string2time(tstamp)
        fname = coils.time2fname(tstamp) + '.jpg'
        dest_dir = os.path.join(self._config['pics_dir'], coils.time2dir(tstamp))
        dest_fname = os.path.join(
            dest_dir,
            fname,
            )
        if os.path.exists(dest_fname):
            print('Skipping {}'.format(dest_fname))
            return    
        try:
            os.makedirs(dest_dir)
        except os.error:
            pass
        saved = os.getcwd()
        os.chdir(dest_dir)
        url = '{}/pics/{}.jpg'.format(
            self._url,
            coils.time2fname(tstamp, full=True),
            )
        print(url)
        wget.download(url, bar=None)
        os.chdir(saved)

        # Propagate timestamp downstream.
        return tstamp


class Viewer(mpipe.OrderedWorker):
    """Displays image in a window."""

    def __init__(self, speedup=1.0):
        self._speedup = speedup
        self._prev_tstamp = dt.datetime.max
        self._prev_dotask = dt.datetime.max
        cv2.namedWindow('wabbit', cv2.cv.CV_WINDOW_NORMAL)

    def doTask(self, (tstamp, image)):

        # Compute time difference between timestamps.
        diff_tstamp = tstamp - self._prev_tstamp
        self._prev_tstamp = tstamp
        diff_tstamp = diff_tstamp.total_seconds()
        diff_tstamp = max(0, diff_tstamp)
        diff_tstamp /= self._speedup

        # Compute time elapsed since previous doTask().
        elapsed = dt.datetime.now() - self._prev_dotask
        elapsed = elapsed.total_seconds()
        elapsed = max(0, elapsed)
        
        # Pause to match real framerate.
        sleep_time = diff_tstamp - elapsed
        if sleep_time < 0:
            self._prev_dotask = dt.datetime.now()
            return
        time.sleep(sleep_time)
        self._prev_dotask = dt.datetime.now()

        try:
            cv2.imshow('wabbit', image)
            cv2.waitKey(1)
        except:
            print('Error in viewer !!!')
