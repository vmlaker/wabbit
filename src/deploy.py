"""
Deploy Wabbit web app to Apache.
"""

from subprocess import call
import os
import sys
import coils

def run(cmd):
    print(cmd)
    call(cmd, shell=True)

# Read command-line parameters and load the config file.
# Usage:  deploy.sh www_root config_file
WWW_ROOT = sys.argv[1]
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.conf'
config = coils.Config(CONFIG)

# Create destination directory and copy the web service source code.
cmd = 'mkdir -p {}'.format(os.path.join(WWW_ROOT, 'service'))
run(cmd)
dest = os.path.join(WWW_ROOT, 'service')
for item in ('templates', 'static'):
    cmd = 'cp -r {} {}'.format(item, dest)
    run(cmd)
 
# Make soft links.
for item in (
    os.path.join('service', 'templates', 'index.html'),
    os.path.join('service', 'templates', 'browser.html'),
    os.path.join('service', 'templates', 'main.css'),
    os.path.join('service', 'templates', 'index.css'),
    os.path.join('service', 'static', 'main.js'),
    os.path.join('service', 'static', 'browser.js'),
    os.path.join('service', 'static', 'logo_small.png'),
    ):
    cmd = 'ln -s {} {}'.format(item, WWW_ROOT)
    run(cmd)
    
# Create the pics/ link.
cmd = 'ln -s {} {}'.format(
    config['pics_dir'], 
    os.path.join(WWW_ROOT, 'pics'))
run(cmd)

# Print HTTPD configuration snippet.
print('')
print('Add the following to your httpd config, then restart httpd:')
text = """
    ################################
    #
    #  Wabbit configuration.
    #
    ################################
    <Directory {pics_dir}>
        Options +Indexes
        Order allow,deny
        Allow from all
        IndexStyleSheet /{db_name}/index.css
        IndexOptions HTMLTable
        IndexOptions NameWidth=*
        IndexOptions FancyIndexing
        IndexOptions SuppressDescription
        IndexOptions SuppressLastModified
        IndexOptions IconsAreLinks
    </Directory>

    ProxyRequests Off
    <Location /wabbit/service>
         ProxyPass http://localhost:8000
         ProxyPassReverse http://localhost:8000
    </Location>

    RewriteEngine On
    RewriteRule /wabbit/browser$ /wabbit/browser.html
    RewriteRule /wabbit/live$ /wabbit [R]

""".format(
    db_name=config['db_name'],
    service_dir=os.path.join(WWW_ROOT, 'service'),
    pics_dir=os.path.join(WWW_ROOT, 'pics'),
    )
print(text)
