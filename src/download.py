"""Download images from remote server.
Parameters:  <begin_time> <length_sec> <url> <config_file>
"""

# Import standard modules.
import os
import sys
import urllib
import urllib2
import simplejson as json

# Import 3rd party modules.
import mpipe
import coils

# Import local modules.
from mpipe_stages import Downloader, DbWriter

# Read command-line parameters.
BEGIN = sys.argv[1]
LENGTH = int(sys.argv[2])
URL = sys.argv[3]
CONFIG = sys.argv[4]

# Load configuration file.
config = coils.Config(CONFIG)

# Assemble the pipeline.
pipe = mpipe.Pipeline(
    mpipe.Stage(Downloader, 8, config=config, url=URL).link(
        mpipe.Stage(DbWriter, 8, config=config)))

# Retrieve timestamps from server.
args = { 'begin' : BEGIN, 'length' : LENGTH }
data = urllib.urlencode(args)
url = '{}/service/tstamps?{}'.format(URL, data)
response = urllib.urlopen(url)
result = json.loads(response.read())
times = result['images']

# Operate the pipeline.
print('Downloading {} images to {}.'.format(len(times), config['pics_dir']))
for time in times:
    pipe.put(time)
pipe.put(None)
