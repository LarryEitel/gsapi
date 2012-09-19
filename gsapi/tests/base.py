# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import sys, os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + os.sep + 'gsapi')
# # sys.path.insert(0, os.sep.join(os.getcwd().split(os.sep)[:-1]))
# # sys.path.insert(0, os.sep.join(__file__.split(os.sep)[:-1]))

import os
import base64
import json

from flask import session

import gsapi.run as run
from flask import current_app
from gsapi.db import get_db
from gsapi.utils import load_data

class TestCase(unittest.TestCase):

    def setUp(self):
        app = run.app
        self.host = app.config['TESTING_HOST']
        app.config['TESTING'] = True
        app = app.test_client()

        db = get_db(app.application)

        # delete existing test db
        db.connection.drop_database(db.name)

        # recreate
        self.db = get_db(app.application)
        self.app = app

    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()
        
    def load_sample(self, filename):
        path = os.sep.join(__file__.split(os.sep)[:-1])

        json_fName = path + '/data/%s.json' % filename

        return load_data(self.db, json_fName)
    
if __name__ == "__main__":
    unittest.main()
