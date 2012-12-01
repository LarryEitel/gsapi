# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase
from utils.utils import mongo_json_object_hook

from bson.json_util import dumps, loads
import json
#from json import loads, dumps
import os
import hashlib
import time
import datetime
import dateutil.parser
from flask import request
from gsapi import models
from pprint import pprint as P
import requests as R # http://docs.python-requests.org/en/latest/
# nosetests gsapi/tests/usecases/test_usecases_initial.py
class TestUseCaseAppKey(TestCase):

    def InsertAppId(self, _c, data, verbose=True):
        dumps_data = dumps(data)
        print "<pre>requests.post('http://" + self.host + '/' + _c + "', data='" + dumps_data + "')</pre>"

        rs = self.app.post('/'+_c, data=dumps_data)

        err = "\nInsertCnt of %s FAILED!" % _c

        if rs.status == 200:
            data = json.loads(rs.data)
            doc = data['docs'][0]['doc']
            m = getattr(models, _c)(**doc)
            if verbose:
                print m.dNam

            return m
        elif rs.status == 400:
            data = json.loads(rs.data)
            print err
            print data['errors'][0]['errors']
            print
            assert False
        else:
            print err
            assert False




    # Flask sessions = {'sessionKey':val}
    def test_one(self):
        print "\n\nTestUseCaseAppKey.test_one\n"

        ''' 
        Explore Facebook like oauth2
        Create AppId doc
        Generate key, app_id

        WebApp wants to call api
            POST /Prs

        Wrap POST with auth required permission
        '''