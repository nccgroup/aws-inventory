import json
import sys

# Tool to read through a response JSON file and print APIs with responses having an item count
# greater than a specified threshold.

JSON_FILE = sys.argv[1]
MAX_NUM_CHILDREN = int(sys.argv[2])

def parse_data(py_obj):
    def parse_children(obj, path):
        if len(path) > 4:
            # not interested in digging into API response objects
            return
        elif len(path) == 4:
            # interested in API responses
            try:
                size = len(obj) if not isinstance(obj, basestring) else 0
                if size > MAX_NUM_CHILDREN:
                    print '.'.join(path)
            except TypeError:
                pass
            return

        if isinstance(obj, dict):
            for key, val in obj.items():
                parse_children(val, path + [str(key)])
        elif isinstance(obj, (list, tuple)):
            for val in obj:
                parse_children(val, path + [str(val)])

    parse_children(py_obj, [])

parse_data(json.load(open(JSON_FILE, 'r')))
