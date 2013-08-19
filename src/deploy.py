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
    os.path.join('service', 'templates', 'browser.html'),
    os.path.join('service', 'templates', 'main.css'),
    os.path.join('service', 'templates', 'index.css'),
    os.path.join('service', 'static', 'main.js'),
    os.path.join('service', 'static', 'browser.js'),
    os.path.join('service', 'static', 'logo_small.png'),
    ):
    cmd = 'ln -s {} {}'.format(item, WWW_ROOT)
    print(cmd); call(cmd, shell=True)
    
# Print HTTPD configuration snippet.
print('')
print('Add the following to your httpd config, then restart httpd:')
text = """
    ################################
    # Wabbit configuration.
    ################################
    WSGIDaemonProcess {db_name} \\
        home={service_dir} \\
        python-path={service_dir}
    WSGIProcessGroup {db_name}
    WSGIScriptAlias /{db_name}/service {service_dir}/wabbit.wsgi
    <Directory {service_dir}>
        Order allow,deny
        Allow from all
    </Directory>
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
""".format(
    db_name=config['db_name'],
    service_dir=os.path.join(WWW_ROOT, 'service'),
    pics_dir=os.path.join(WWW_ROOT, 'pics'),
    )
print(text)
