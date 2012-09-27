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

from pyes.es import ES

from flask import session

import gsapi.run as run
from flask import current_app
from gsapi.db import get_db, get_db2
#from gsapi.db import db
from gsapi.utils import load_data

es_conn = {"host":"localhost", "port":9200}

# get elasticsearch connection
def get_es_conn(*args, **kwargs):
    return ES(("http", es_conn['host'], es_conn['port']), *args, **kwargs)

class TestCase(unittest.TestCase):

    def setUp(self):
        app = run.app
        self.host = app.config['TESTING_HOST']
        app.config['TESTING'] = True
        app = app.test_client()

        dbname = app.application.config['MONGO_TEST_DBNAME']

        db = get_db2(dbname)

        # delete existing test db
        db.connection.drop_database(dbname)
        #app.db = db
        self.db = db

        #db = get_db(app.application)
        # db = app.application.extensions['pymongo']['MONGO'][1]

        # delete existing test db
        #db.connection.drop_database(dbname)

        # recreate
        #self.db = get_db(app.application)
        # self.db = db.connection.drop_database(db.name)
        self.app = app

        # es = elasticsearch
        es = get_es_conn(timeout=300.0)#incremented timeout for debugging
        self.index_name = "test-index"
        self.document_type = "test-type"
        es.delete_index_if_exists(self.index_name)
        # es.create_index(self.index_name)
        self.es = es


    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()

        # self.es.delete_index_if_exists(self.index_name)

    def load_sample(self, filename):
        path = os.sep.join(__file__.split(os.sep)[:-1])

        json_fName = path + '/data/%s.json' % filename

        return load_data(self.db, json_fName)

if __name__ == "__main__":
    unittest.main()
