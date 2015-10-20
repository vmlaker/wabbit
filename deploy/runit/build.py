"""
Create runit files from .in templates.
"""

from os import chdir
from os.path import dirname, join, normpath, realpath
import glob
import getpass
import sys
import subprocess

import coils

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.conf'
config = coils.Config(CONFIG)

# Do the work in the directory of this file.
this_dir = dirname(realpath(__file__))
chdir(this_dir)

# Get the path to the root Wabbit directory.
root_dir = normpath(join(this_dir, '..', '..'))

# Add items to configuration.
for key, val in {
    'WORKING_DIR' : root_dir,
    'RECORD_CMD'  : normpath(join(root_dir, 'bin', 'record')),
    'PYTHON'      : normpath(join(root_dir, 'python')),
    'PRUNER'      : normpath(join(root_dir, 'src', 'py', 'pruner.py')),
    'GUNICORN_BIN': normpath(join(root_dir, 'venv', 'bin', 'gunicorn')),
    'APP_MODULE'  : 'src.py.serve:app',
    'USER'        : getpass.getuser(),
    'GROUP'       : getpass.getuser(),
    'BASH'        : subprocess.check_output(('which', 'bash')).strip(),
}.items():
    config[key] = val

# For each *.runit.in template, create a real .runit
# file with text replacement as per the configuration.
for fname in glob.glob('*.runit.in'):
    outf = config['db_name'] + '-' + fname[:-3]
    print('Building {}'.format(outf))
    with open(fname) as inf:
        with open(outf, 'w') as outf:
            for line in inf.readlines():
                for key, val in config.items():
                    line = line.replace('@{}@'.format(key), val)
                outf.write(line)
