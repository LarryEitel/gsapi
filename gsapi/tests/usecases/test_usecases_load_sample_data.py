# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase
import json
import time
import isodate
from flask import request
from random import randint
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
from pyes import TermQuery
from gsapi import models
from gsapi import controllers
import time
class TestUseCaseLoadSampleData(TestCase):
    def test_initial(self):
        es              = self.es
        es_index_name   = es.__dict__['index_name']
        generic = controllers.Generic(self.db, es)

        args    = {
            'class_name': 'Usr',
            'docs': [{
                "uNam"  :"jkutz", "fNam"  :"Josh", "lNam"  :"Kutz", "gen"   :'m', "emails": [{"email" : "josh@kutz.com"}]
            }]
        }
        rs           = generic.post(**args)
        assert rs['status_code'] == 200 and rs['response']['total_inserted'] == 1
        doc = rs['response']['docs'][0]['doc']


        #time.sleep(1)
        es.refresh(es_index_name)
        q = TermQuery("dNam", "josh")
        results = es.search(query = q)

        x=0
