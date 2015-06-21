"""
Remove Wabbit Systemd service from system.
"""

from glob import glob
from os import chdir, remove
from os.path import dirname, join, realpath
from subprocess import call
import sys

import coils

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.conf'
config = coils.Config(CONFIG)

# Do the work in the directory of this file.
this_dir = dirname(realpath(__file__))
chdir(this_dir)

for service in glob('*.service'):
    print('Stopping {}'.format(service))
    call('systemctl stop {}'.format(service), shell=True)
    print('Disabling {}'.format(service))
    call('systemctl disable {}'.format(service), shell=True)
    fname = join('/lib/systemd/system', service)
    print('Deleting file {}'.format(fname))
    try:
        remove(fname)
    except OSError:
        pass
    print('Deleting file {}'.format(service))
    try:
        remove(service)
    except OSError:
        pass
