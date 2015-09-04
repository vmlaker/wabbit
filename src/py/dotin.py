"""
Process the template file by replacing @*@ strings
with settings in config file, and print result to stdout.
"""
usage = \
"""\
Usage:  python dotin.py input_file [<config_file>]\
"""

import sys
import coils

# Parse input parameters.
try:
    input_file = sys.argv[1]
except IndexError:
    print(usage)
    sys.exit(1)

# Load configuration file.
CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.conf'
config = coils.Config(CONFIG)

# Perform string replacement, line by line.
with open(input_file) as inf:
    for line in inf:
        for key, val in config.items():
            line = line.replace('@{}@'.format(key), val)
        line = line.rstrip('\n')
        print(line)
