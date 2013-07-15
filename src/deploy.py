"""Deploy app to Apache."""

from subprocess import call
import os
import sys
import coils

www_root = sys.argv[1]

# Load configuration file.
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.cfg'
config = coils.Config(CONFIG)

cmd = 'mkdir {}'.format(www_root)
print(cmd)
call(cmd, shell=True)

cmd = 'ln -s {} {}'.format(
    config['pics_dir'], 
    os.path.join(www_root, 'pics'))
print(cmd)
call(cmd, shell=True)

cmd = 'cp -r . {}'.format(os.path.join(www_root, 'service'))
print(cmd)
call(cmd, shell=True)

cmd = 'ln -s {} {}'.format(
    os.path.join('service', 'templates', 'index.html'),
    os.path.join(www_root))
print(cmd)
call(cmd, shell=True)

cmd = 'ln -s {} {}'.format(
    os.path.join('service', 'static', 'main.js'),
    os.path.join(www_root))
print(cmd)
call(cmd, shell=True)

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
    os.path.join(www_root, 'service', 'wabbit.wsgi'),
    os.path.join(www_root, 'service'),
    os.path.join(www_root, 'pics'),

    )
print httpd
