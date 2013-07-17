"""Various MPipe stages."""

import os
import cv2
import sqlalchemy as sa
import wget
import mpipe
import coils
import mapping


class DiskSaver(mpipe.UnorderedWorker):
    """Saves file to disk."""

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
        fname = os.path.join(dname, coils.time2fname(tstamp)) + '.' + self._config['f_ext']
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
        fname = coils.time2fname(tstamp) + '.' + self._config['f_ext']
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
        url = '{}/pics/{}.{}'.format(
            self._url,
            coils.time2fname(tstamp, full=True),
            self._config['f_ext'],
            )
        print(url)
        wget.download(url, bar=None)
        os.chdir(saved)

        # Propagate timestamp downstream.
        return tstamp
