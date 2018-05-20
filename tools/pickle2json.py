import datetime
import json
import pickle
import sys

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super(DateTimeEncoder, self).default(o)

print json.dumps(pickle.load(open(sys.argv[1], 'rb')), cls=DateTimeEncoder)
