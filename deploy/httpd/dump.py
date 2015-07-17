"""
Dump Apache HTTPD configuration to stdout.
"""

from os import chdir
from os.path import dirname, join, normpath, realpath
import sys

import coils

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.conf'
config = coils.Config(CONFIG)

# Go into the directory of this file.
this_dir = dirname(realpath(__file__))
chdir(this_dir)

# Create a httpd.conf file with text replacement as per the configuration.
with open('httpd.conf.in') as inf:
    for line in inf.readlines():
        line = line.rstrip()
        for key, val in config.items():
            line = line.replace('@{}@'.format(key), val)
        print(line)
