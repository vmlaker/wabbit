"""Deploy app to Apache."""

from subprocess import call
import os
import sys
import coils

# Read command-line parameters.
WWW_ROOT = sys.argv[1]
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.cfg'

# Load configuration file.
config = coils.Config(CONFIG)

# Create destination directories.
cmd = 'mkdir -p {}'.format(os.path.join(WWW_ROOT, 'service'))
print(cmd); call(cmd, shell=True)

# Create the pics/ link.
cmd = 'ln -s {} {}'.format(
    config['pics_dir'], 
    os.path.join(WWW_ROOT, 'pics'))
print(cmd); call(cmd, shell=True)

# Copy source code.
dest = os.path.join(WWW_ROOT, 'service')
for item in ('src', 'templates', 'static', 'wabbit.cfg', 'wabbit.wsgi'):
    cmd = 'cp -r {} {}'.format(item, dest)
    print(cmd); call(cmd, shell=True)
 
# Make soft links.
for item in (
    os.path.join('service', 'templates', 'index.html'),
    os.path.join('service', 'templates', 'main.css'),
    os.path.join('service', 'static', 'main.js'),
    os.path.join('service', 'static', 'logo_small.png'),
    ):
    cmd = 'ln -s {} {}'.format(item, WWW_ROOT)
    print(cmd); call(cmd, shell=True)
    
# Print HTTPD configuration snippet.
print('')
print('Add the following to your httpd config, then restart httpd:')
httpd = """
    WSGIScriptAlias /{0}/service {1}
    <Location {2}>
        Allow from all
        Order allow,deny
    </Location>
    <Location {3}>
        Options Indexes FollowSymLinks
        Allow from all
        Order allow,deny
    </Location>
""".format(
    config['db_name'],
    os.path.join(WWW_ROOT, 'service', 'wabbit.wsgi'),
    os.path.join(WWW_ROOT, 'service'),
    os.path.join(WWW_ROOT, 'pics'),

    )
print(httpd)
