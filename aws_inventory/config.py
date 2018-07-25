"""Configuration parameters affecting tool operation."""

import multiprocessing
import re
import string


# max number of threads for invoking APIs of a service in a region
MAX_THREADS = multiprocessing.cpu_count() * 2

# RE to filter desired service operation names
SVC_OPS_RE = re.compile(r'^(Describe|List).+')

## some constants ##

# used to create JSON file (in "./gui/") for holding the GUI data
GUI_DATA_FILENAME_TEMPLATE = string.Template('gui/aws_inventory_data-$profile.json')

## Network-related timeouts. See botocore/endpoint.py ##
# number of seconds to wait for a connection to succeed. By default, botocore tries 4 times.
CLIENT_CONNECT_TIMEOUT = 10
# number of seconds to wait for a complete API response to be received
CLIENT_READ_TIMEOUT = 10

# region to use when service model says there are no regions, but creating a client still
# requires one
DEFAULT_REGION = 'us-west-2'
