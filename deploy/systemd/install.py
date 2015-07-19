"""
Install Wabbit Systemd service.
"""

from glob import glob
from shutil import copy
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

dst = '/lib/systemd/system'
for fname in glob('{}*.service'.format(config['db_name'])):
    print('Copying {} to {}'.format(fname, dst))
    copy(fname, dst)
    print('Enabling {}'.format(fname))
    call('systemctl enable {}'.format(fname), shell=True)
