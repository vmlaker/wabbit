"""
Create soft link to pictures directory.
"""

import os
from os.path import join, realpath
import sys

import coils

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.conf'
config = coils.Config(CONFIG)

source = realpath(config['pics_dir'])
link = config['db_name'] + '_pics'
link = join('/', 'var', 'www', 'html', link)

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
