"""
The code which mod_wsgi executes upon startup.
"""

# Change this to location of your app:
WABBIT = '/var/www/html/wabbit/service'

# Add the application to the Python load path.
import sys
sys.path.insert(0, WABBIT)

# Application is intended to run in it's directory.
import os
os.chdir(WABBIT)

# Set variable "application" to the app object.
from serve import app as application

