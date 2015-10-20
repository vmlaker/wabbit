"""
Stop the Wabbit runit services.
"""

from glob import glob
from os import chdir
from os.path import dirname, realpath
from subprocess import call
from sys import argv
from coils import Config

# Load configuration file.
config_fname = argv[1] if len(argv)>=2 else 'wabbit.conf'
config = Config(config_fname)

# Do the work in the directory of this file.
this_dir = dirname(realpath(__file__))
chdir(this_dir)

for fname in glob('*.runit'):
    name = fname[:fname.find('.runit')]
    print('Stopping service {}'.format(name))
    call('sv stop {}'.format(name), shell=True)
