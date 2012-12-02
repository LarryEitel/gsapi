# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import run
from pymongo import Connection
import globals

# get elasticsearch connection
def get_es_conn(*args, **kwargs):
    if 'cfg' in kwargs:
        cfg = kwargs['cfg']
        kwargs.pop('cfg')
    else:
        cfg = {'host': 'localhost', 'port': 9200}

    return ES(("http", cfg['host'], cfg['port']), *args, **kwargs)

class TestCase(unittest.TestCase):
    tests_data_yaml_dir = 'tests/data/yaml/'
    def setUp(self):
        app                   = run.app
        app.config['TESTING'] = True
        self.host             = app.config['TESTING_HOST']
        
        self.app              =  app.test_client()
        self.g                = globals.load()
        self.g['usr']         = {"OID": "50468de92558713d84b03fd7", "at": (-84.163063, 9.980516)}

    def tearDown(self):
        pass
class MongoTestCase(TestCase):
    def setUp(self):
        super(MongoTestCase, self).setUp()
        
        dbhost = self.app.application.config['MONGO_HOST']
        dbname = self.app.application.config['MONGO_TEST_DBNAME']
        db     = Connection(dbhost)[dbname]

        # delete existing test db
        db.connection.drop_database(dbname)

        # recreate
        db           = Connection(dbhost)[dbname]
        
        # at location lnglat - lattitude, longitude (x,y) per: https://github.com/j2labs/schematics/blob/master/schematics/base.py
        self.g['db'] = db
        self.g['es'] = None
    def tearDown(self):
        pass
        # clean after testing
        #models.db.session.remove()

        # self.es.delete_index_if_exists(self.index_name)

if __name__ == "__main__":
    unittest.main()
