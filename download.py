"""Download images from remote server.
Parameters:  <begin_time> <length_sec> <url> <dest_dir>
"""

import os
import sys
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
    dest = os.path.join(DEST, coils.time2dir(tstamp))
    try:
        os.makedirs(dest)
    except os.error:
        pass
    saved = os.getcwd()
    os.chdir(dest)
    fname = coils.time2fname(tstamp) + '.png'
    if os.path.exists(fname):
        return
    fname = coils.time2fname(tstamp, full=True) + '.png'
    url = '{}/pics/{}'.format(URL, fname)
    wget.download(url, bar=None)
    os.chdir(saved)

# Assemble the pipeline.
pipe = mpipe.Pipeline(mpipe.UnorderedStage(download, 8))

# Retrieve timestamps from server.
url = '{}/service/tstamps?begin={}&length={}'.format(
    URL, BEGIN, LENGTH)
print(url)
f = urllib2.urlopen(url)
result = json.loads(f.read())
times = result['images']

# Operate the pipeline.
print('Downloading {} images to {}.'.format(len(times), DEST))
for time in times:
    pipe.put(time)
pipe.put(None)
