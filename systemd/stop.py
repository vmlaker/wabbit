"""
Stop the Wabbit Systemd service.
"""

from glob import glob
from os import chdir
from os.path import dirname, realpath
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
    print('Stopping service {}'.format(service))
    call('systemctl stop {}'.format(service), shell=True)
