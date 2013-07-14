"""Download images from remote server.
Parameters:  <begin_time> <length_sec> <url> <dest_dir>
"""

import os
import sys
import urllib
import urllib2
import simplejson as json
import mpipe
import wget
import coils

# Read command-line parameters.
BEGIN = sys.argv[1]
LENGTH = int(sys.argv[2])
URL = sys.argv[3]
DEST = sys.argv[4]

def download(tstamp):
    """Download image."""
    tstamp = coils.string2time(tstamp)
    fname = coils.time2fname(tstamp) + '.png'
    dest_dir = os.path.join(DEST, coils.time2dir(tstamp))
    dest_fname = os.path.join(
        dest_dir,
        fname,
        )
    if os.path.exists(dest_fname):
        print('Skipping {}'.format(dest_fname))
        return    
    try:
        os.makedirs(dest_dir)
    except os.error:
        pass
    saved = os.getcwd()
    os.chdir(dest_dir)
    url = '{}/pics/{}'.format(URL, coils.time2fname(tstamp, full=True) + '.png')
    print(url)
    wget.download(url, bar=None)
    os.chdir(saved)

# Assemble the pipeline.
pipe = mpipe.Pipeline(mpipe.UnorderedStage(download, 8))

# Retrieve timestamps from server.
args = { 'begin' : BEGIN, 'length' : LENGTH }
data = urllib.urlencode(args)
url = '{}/service/tstamps?{}'.format(URL, data)
response = urllib.urlopen(url)
result = json.loads(response.read())
times = result['images']

# Operate the pipeline.
print('Downloading {} images to {}.'.format(len(times), DEST))
for time in times:
    pipe.put(time)
pipe.put(None)
