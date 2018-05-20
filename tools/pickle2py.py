import pickle
import pprint
import sys

obj = pickle.load(open(sys.argv[1], 'rb'))
pprint.pprint(obj)
