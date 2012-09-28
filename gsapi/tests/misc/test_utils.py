# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase
import json
import time
from bson import ObjectId


#TODO: Test validation
class TestUtils(TestCase):
    def test_load_data(self):
        print "\nTestUtils.test_load_data"
        print """LOAD SAMPLE DOCS:\n"""

        from gsapi.utils import load_data

        json_fname = 'contacts'
        resp = self.load_sample(json_fname)

        print "From: {json_fname}, {count} docs loaded, {errors} errors.".format(json_fname=json_fname, count=resp['response']['total_inserted'], errors=resp['response']['total_invalid'])
        if not resp['status'] == 200:
            print resp

        assert resp['status'] == 200

if __name__ == "__main__":
    unittest.main()
