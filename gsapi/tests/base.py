# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import sys, os

sys.path.insert(0, "..")
sys.path.insert(0, os.getcwd() + os.sep + 'gsapi')
# # sys.path.insert(0, os.sep.join(os.getcwd().split(os.sep)[:-1]))
# # sys.path.insert(0, os.sep.join(__file__.split(os.sep)[:-1]))

import os
import base64
import json

from pyes.es import ES

from flask import session

import gsapi.run as run
from gsapi.utils import load_data
from pymongo import Connection

# get elasticsearch connection
def get_es_conn(*args, **kwargs):
    if 'cfg' in kwargs:
        cfg = kwargs['cfg']
        kwargs.pop('cfg')
    else:
        cfg = {'host': 'localhost', 'port': 9200}

    return ES(("http", cfg['host'], cfg['port']), *args, **kwargs)

class TestCase(unittest.TestCase):

    def setUp(self):
        app = run.app
        self.host = app.config['TESTING_HOST']
        app.config['TESTING'] = True

        # es = elasticsearch
        es_cfg = {
            'host': app.config['ES_TEST_HOST'],
            'port': app.config['ES_TEST_PORT'],
            'name': app.config['ES_TEST_NAME']
            }

        app = app.test_client()

        dbhost = app.application.config['MONGO_HOST']
        dbname = app.application.config['MONGO_TEST_DBNAME']
        db = Connection(dbhost)[dbname]

        # delete existing test db
        db.connection.drop_database(dbname)

        # recreate
        db = Connection(dbhost)[dbname]
        self.db = db
        self.app = app

        es = get_es_conn(cfg=es_cfg, timeout=300.0)#incremented timeout for debugging
        self.index_name = es_cfg['name']
        es.__dict__['index_name'] = es_cfg['name']
        self.document_type = "test-type"
        es.delete_index_if_exists(self.index_name)
        es.create_index(self.index_name)
        self.es = es

    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()

        # self.es.delete_index_if_exists(self.index_name)

    def load_sample(self, filename):
        path = os.sep.join(__file__.split(os.sep)[:-1])

        json_fName = path + '/data/%s.json' % filename

        return load_data(self.db, self.es, json_fName)

if __name__ == "__main__":
    unittest.main()
