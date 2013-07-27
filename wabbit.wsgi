"""
The code which mod_wsgi executes upon startup.
Sets variable "application" to the app object.
"""

from src.serve import app as application
