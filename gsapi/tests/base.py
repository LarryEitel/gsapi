# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import sys, os

#sys.path.insert(0, "..")
#sys.path.insert(0, os.getcwd() + os.sep + 'gsapi')
#sys.path.insert(0, os.sep.join(os.getcwd().split(os.sep)[:-1]))
#sys.path.insert(0, os.sep.join(__file__.split(os.sep)[:-1]))

import os
import base64
import json

from flask import session

import run as run
import models
from utils.utils import load_data
from pymongo import Connection

# get elasticsearch connection
def get_es_conn(*args, **kwargs):
    if 'cfg' in kwargs:
        cfg = kwargs['cfg']
        kwargs.pop('cfg')
    else:
        cfg = {'host': 'localhost', 'port': 9200}

    return ES(("http", cfg['host'], cfg['port']), *args, **kwargs)

class MongoTestCase(unittest.TestCase):

    def setUp(self):
        app                   = run.app
        app.config['TESTING'] = True
        self.host             = app.config['TESTING_HOST']

        app    = app.test_client()
        
        dbhost = app.application.config['MONGO_HOST']
        dbname = app.application.config['MONGO_TEST_DBNAME']
        db     = Connection(dbhost)[dbname]

        # delete existing test db
        db.connection.drop_database(dbname)

        # recreate
        db       = Connection(dbhost)[dbname]
        self.db  = db
        self.app = app

        # at location lnglat - lattitude, longitude (x,y) per: https://github.com/j2labs/schematics/blob/master/schematics/base.py
        self.usr = {"OID": "50468de92558713d84b03fd7", "at": (-84.163063, 9.980516)} 
    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()

        # self.es.delete_index_if_exists(self.index_name)
class TestCase(unittest.TestCase):

    def setUp(self):
        app                   = run.app
        app.config['TESTING'] = True
        self.host             = app.config['TESTING_HOST']

        # es = elasticsearch
        #es_cfg = app.config['ES_TEST']

        app    = app.test_client()
        
        dbhost = app.application.config['MONGO_HOST']
        dbname = app.application.config['MONGO_TEST_DBNAME']
        db     = Connection(dbhost)[dbname]

        # delete existing test db
        db.connection.drop_database(dbname)

        # recreate
        db       = Connection(dbhost)[dbname]
        self.db  = db
        self.app = app
        # at location lnglat - lattitude, longitude (x,y) per: https://github.com/j2labs/schematics/blob/master/schematics/base.py
        self.usr = {"OID": "50468de92558713d84b03fd7", "at": (-84.163063, 9.980516)} 

        #es = get_es_conn(cfg=es_cfg, timeout=300.0)#incremented timeout for debugging
        #self.index_name = es_cfg['name']
        #es.__dict__['index_name'] = es_cfg['name']
        #self.document_type = "test-type"
        #es.delete_index_if_exists(self.index_name)
        #es.create_index(self.index_name)

        ## es.put_mapping('Prs', {'properties':models.esCnt}, [self.index_name])

        #self.es = es

    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()

        # self.es.delete_index_if_exists(self.index_name)

if __name__ == "__main__":
    unittest.main()
