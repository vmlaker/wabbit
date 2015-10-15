"""
Dump Apache HTTPD configuration to stdout.
"""

from os import chdir
from os.path import dirname, join, normpath, realpath
import sys

import coils

www_directory = sys.argv[1]
config_fname = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.conf'

# Load the configuration, and add to it path to www.
config = coils.Config(config_fname)
config['www_directory'] = normpath(www_directory)

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
