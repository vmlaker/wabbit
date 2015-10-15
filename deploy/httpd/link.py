"""
Create soft link to the pictures directory
inside HTTPD www directory.
"""

import os
from os.path import join, realpath
import sys

import coils

www_directory = sys.argv[1]
config_fname = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.conf'

config = coils.Config(config_fname)
source = realpath(config['pics_dir'])
link = config['db_name'] + '_pics'
link = join(www_directory, link)

# Remove soft link if already exists.
try:
    os.remove(link)
except OSError:
    pass

# Create the soft link.
print('Linking source={}, link={}'.format(source, link))
try:
    os.symlink(source, link)
except OSError as ose:
    print(ose)
    sys.exit(1)
