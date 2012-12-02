# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from tests.base import TestCase
from utils import myyaml
# http://pyyaml.org/wiki/PyYAMLDocumentation

class TestMyYaml(TestCase):
    tests_data_yaml_dir = 'tests/data/yaml/'
    def test_parse_file(self):
        '''Doc this
            '''
        obj = myyaml.pyObj(self.tests_data_yaml_dir + 'cnts' + '.yaml')
        assert True
        
if __name__ == "__main__":
    unittest.main()
