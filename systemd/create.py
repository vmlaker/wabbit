"""
Create systemd files from .in templates.
"""

import os
import glob
import getpass

# Do the work in the directory of this file.
this_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(this_dir)

# Create the configuration dict.
config = {
    'WORKING_DIR' : os.path.join(this_dir, '..'),
    'RECORD_CMD'  : os.path.join(this_dir, '..', 'bin', 'record'),
    'GUNICORN_BIN': os.path.join(this_dir, '..', 'venv', 'bin', 'gunicorn'),
    'APP_MODULE'  : 'src.serve:app',
    'ADDRESS'     : '127.0.0.1:8000',
    'USER'        : getpass.getuser(),
    'GROUP'       : getpass.getuser(),
}

# For each *.service.in template, create a real .service 
# file with text replacement as per the configuration.
for fname in glob.glob('*.service.in'):
    with open(fname) as inf:
        outf = fname[:-3]
        with open(outf, 'w') as outf:
            for line in inf.readlines():
                for key, val in config.items():
                    line = line.replace('@{}@'.format(key), val)
                outf.write(line)
