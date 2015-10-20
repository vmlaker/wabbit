"""
Install Wabbit runit services.
"""

from glob import glob
from shutil import copy
from os import chdir
from os.path import dirname, realpath
from subprocess import call
import sys
import os
import stat
import getpass
import pwd

import coils

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.conf'
config = coils.Config(CONFIG)

# Do the work in the directory of this file.
this_dir = dirname(realpath(__file__))
chdir(this_dir)

for source in glob('{}*.runit'.format(config['db_name'])):
    name = source[:source.find('.runit')]
    dirname = os.path.join('/', 'etc', 'sv', name)
    print('Creating directory {}'.format(dirname))
    try:
        os.mkdir(dirname)
    except OSError:
        print('Directory already exists.')
    dest = os.path.join(dirname, 'run')
    print('Copying {} to {}'.format(source, dest))
    copy(source, dest)
    print('Chmodding {} to EXEC'.format(dest))
    os.chmod(dest, stat.S_IEXEC)
    target = os.path.join('/', 'etc', 'service', name)
    print('Symlinking source={} to target={}'.format(dirname, target))
    try:
        os.symlink(dirname, target)
    except OSError:
        print('Symlink already exists.')
    for name in 'ok', 'control', 'status':
        continue
        target = os.path.join(dirname, 'supervise', name)
        username = getpass.getuser()
        print('Chowning {} to {}'.format(target, username))
        os.chown(
            target, 
            pwd.getpwnam(getpass.getuser()).pw_uid,
            pwd.getpwnam(getpass.getuser()).pw_gid,
        )
