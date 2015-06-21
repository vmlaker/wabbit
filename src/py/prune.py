"""Prune database and disk of old images.

Disk is pruned to the next 60 s boundary. 
To prune all files use seconds value <= -60.

"""
usage = \
"""
Usage:  python prune.py  <older_than_sec> [<config_file>]
"""

import sys
import coils
import pruner

# Read command-line parameters.
try:
    SECONDS = float(sys.argv[1])
    CONFIG = sys.argv[2] if len(sys.argv)>=3 else 'wabbit.conf'
except:
    print(usage)
    sys.exit(1)

# Load configuration file.
config = coils.Config(CONFIG)

# Override history length.
config['max_history'] = SECONDS

# Prune.
pruner = pruner.Pruner(config)
pruner.prune()
