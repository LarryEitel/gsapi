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

class TestGeneric(MongoTestCase):
    print "Generic tests"
    print "=============="
    _c = 'Prs'

    def test_post_nextId(self):
        print
        print "Post nextId"
        print "^^^^^^^^^^^^"

        db = self.db
        generic = controllers.Generic(db)

        # here is the basic function call being tested
        fn = "controllers.generic.get(db, **args)"

        # POST ONE ################################
        host = self.host
        sample_doc = {
            "fNam":"johnathan",
            "lNam":"doe",
            "mOn": isodate.parse_datetime("2012-09-27T21:43:33.927Z"),
            "oBy": ObjectId("50468de92558713d84b03fd0"),
            "rBy": ObjectId("50468de92558713d84b03fd7"),
            "gen":'m',
            "emails" : [{
                "email" : "john@doe.com"
            }]
        }

        args = {}
        args['_c'] = self._c
        args['docs'] = [sample_doc]

        response = generic.post(**args)

        assert response['status_code'] == 200
        data = response['response']
        got_docs = data['docs']

        assert data['total_inserted'] == 1

        doc = data['docs'][0]['doc']
        id = data['docs'][0]['id']
        assert doc['fNam'] == sample_doc['fNam']

    def test_post(self):
        print
        print "Post one doc"
        print "^^^^^^^^^^^^"

        db = self.db
        generic = controllers.Generic(db)

        # here is the basic function call being tested
        fn = "controllers.generic.get(db, **args)"

        # POST ONE ################################
        host = self.host
        sample_doc = {
            "fNam":"johnathan",
            "lNam":"doe",
            "mOn": isodate.parse_datetime("2012-09-27T21:43:33.927Z"),
            "oBy": ObjectId("50468de92558713d84b03fd0"),
            "rBy": ObjectId("50468de92558713d84b03fd7"),
            "gen":'m',
            "emails" : [{
                "email" : "john@doe.com"
            }]
        }

        args = {}
        args['_c'] = self._c
        args['docs'] = [sample_doc]


        response = generic.post(**args)

        assert response['status_code'] == 200
        data = response['response']
        got_docs = data['docs']

        assert data['total_inserted'] == 1

        doc = data['docs'][0]['doc']
        id = data['docs'][0]['id']
        assert doc['fNam'] == sample_doc['fNam']

if __name__ == "__main__":
    unittest.main()
