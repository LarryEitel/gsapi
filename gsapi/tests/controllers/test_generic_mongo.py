# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
import sys
from tests.base import MongoTestCase
import json
import time
import isodate
import yaml
from random import randint
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import models
import controllers

class TestGenericMongo(MongoTestCase):
    print "Generic tests"
    print "=============="

    def test_post_tmp(self):
        print
        print "Post one tmp doc"
        
        db      = self.db
        generic = controllers.Generic(db)

        sample_doc = {
            "_c": "Prs",
        }
        
        args           = {}
        args['usrOID'] = "50468de92558713d84b03fd7"
        args['docs']   = [sample_doc]
        
        response       = generic.post(**args)

        assert response['status_code'] == 200
        data     = response['response']

        assert data['total_inserted'] == 1
        
        doc = data['docs'][0]['doc']
        assert doc['dId'] > 0
        
        # now let's put some data in and the repost. It should move tmp doc to main collection and delete the temp doc.

        args                 = {}
        args['usrOID']       = "50468de92558713d84b03fd7"
        
        sample_doc           = doc
        sample_doc['prefix'] = 'Mr'
        sample_doc['fNam']   = 'Larry'
        sample_doc['lNam']   = 'King'
        sample_doc['suffix'] = 'Sr'
        args['docs']         = [sample_doc]
        
        response             = generic.post(**args)

        assert response['status_code'] == 200
        data     = response['response']
        
        assert data['total_inserted'] == 1
        doc = data['docs'][0]['doc']
        
        assert doc['fNam'] == sample_doc['fNam']
        assert not 'isTmp' in doc.keys()

        #TODO 
        # Make sure tmp doc was successfully removed

    def test_post(self):
        print
        print "Post one doc"
        
        db      = self.db
        generic = controllers.Generic(db)

        sample_doc = {
            "_c": "Prs",
            "id": 1,
            "fNam": "johnathan",
            "lNam": "doe",
            "gen": 'm'
        }
        
        args           = {}
        args['usrOID'] = "50468de92558713d84b03fd7"
        args['docs']   = [sample_doc]
        
        response       = generic.post(**args)

        assert response['status_code'] == 200
        data     = response['response']
        got_docs = data['docs']

        assert data['total_inserted'] == 1
        
        doc = data['docs'][0]['doc']
        assert doc['fNam'] == sample_doc['fNam']

if __name__ == "__main__":
    unittest.main()
