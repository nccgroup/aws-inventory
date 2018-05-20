import os
import unittest
from StringIO import StringIO

import aws_inventory.invoker


TEST_RESPONSE_STORE = {
    'test-service1': {
        'test-region1': {
            'test-operation1': 'string',
            'test-operation2': 42,
            'test-operation3': {'dict': 'response'},
            'test-operation4': ['element1', 'element2', 'elementN'],
            'test-operation5': [{'key1': 'val1'}, 'val2', {'keyN': 'valN'}]
        },
        'test-region2': {
            'test-operation1': 'string'
        }
    },
    'test-service2': {
        'test-region1': {
            'test-operation1': 'string'
        }
    }
}
for i in range(3, 103):
    TEST_RESPONSE_STORE.update({
        'test-service' + str(i): {
        'test-region1': {
            'test-operation1': 'string'
        }
    }})

TEST_EXCEPTION_STORE = {'test-service': {'test-operation1': {'test-region': 'exception'}}}

class TestDataStore(unittest.TestCase):
    def test_data_file_generation(self):
        responses_dump_fp = StringIO()
        responses_dump_fp.name = '<memory file>'
        exceptions_dump_fp = StringIO()
        exceptions_dump_fp.name = '<memory file>'
        gui_data_fp = open('gui/aws_inventory_data.js', 'w')
        #gui_data_fp = StringIO()
        #gui_data_fp.name = '<memory file>'
        args_dict = {'profile': 'default',
                     'services': 'test-service',
                     'regions': 'test-region',
                     'csv_credentials': None,
                     'mfa_serial': None,
                     'mfa_code': None,
                     'quiet': True,
                     'dry_run': False}
        args = type('TestArgs', (), args_dict)
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_access_key_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_secret_access_key'
        invoker = aws_inventory.invoker.ApiInvoker(args, None, None)
        invoker.store._response_store = TEST_RESPONSE_STORE
        invoker.store._exception_store = TEST_EXCEPTION_STORE
        invoker.write_results(responses_dump_fp, exceptions_dump_fp, gui_data_fp)

if __name__ == '__main__':
    unittest.main()
