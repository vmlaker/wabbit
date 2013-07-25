"""Format for logging handler."""

fields = (
    #  name           size (<0 means unlimited)
    # ----------     ------
    #('asctime'     , '23.23'),
    #('levelname'   , '3.3'),
    #('process'     , '8.8'),
    #('thread'      , '8.8'),
    #('processName' , '15.15'),
    #('module'      , '15.15'),
    #('funcName'    , '8.8'),
    ('message'     , -1),
    )

def getFormat(fields=fields, sep='|'):
    """Return the format string to be used in configuration
    of the logging module."""
    result = ''
    first = True
    for name, size in fields:

        # Append the delimiter between fields.
        result += '' if first else sep
        first = False

        # Append formating for the current field.
        result += '%({})'.format(name)
        result += '-{:s}s'.format(size) if size >= 0 else 's'

    return result
