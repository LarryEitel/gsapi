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
import time
import datetime
import dateutil.parser
from flask import request
from gsapi import models
from pprint import pprint as P
import requests as R # http://docs.python-requests.org/en/latest/
# nosetests gsapi/tests/usecases/test_usecases_initial.py

class TestUseCaseInitial(TestCase):

    def InsertCnt(self, _c, data, verbose=True):
        dumps_data = dumps(data)
        print "<pre>requests.post('http://" + self.host + '/' + _c + "', data='" + dumps_data + "')</pre>"

        rs = self.app.post('/test/'+_c, data=dumps_data)

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

    def test_one(self):
        print "\n\nTestUseCaseInitial.test_one\n"

        print "### CREATE Admin Usr:"
        UsrAdminJosh = self.InsertCnt('Usr', {"uNam":"jkutz", "fNam":"Josh", "lNam":"Kutz", "gen":"m", "emails": [{"email":"josh@kutz.org"}], "grps": ["admin"]})

        print "### ADD Usr:"
        usrMary = self.InsertCnt('Usr', {"uNam":"marys", "fNam":"Mary", "lNam":"Smith", "gen":"f", "emails": [{"email":"mary@gsni.org"}]})

        # rs = R.post('http://localhost:5000/Prs', data='{"fNam":"Freddy", "lNam":"Doe", "gen":"m", "emails": [{"email":"john@doe.com"}]}')
        print "### ADD Prs:"
        prsJohn = self.InsertCnt('Prs', {"fNam":"John", "lNam":"Doe", "gen":"m", "emails": [{"email":"john@doe.com"}]})

        '''
        create Usr
            uNam
            pw
            rBy
        create Cmp GSNI

        Associate Usr with GSNI

        create Prs
            owned by Usr
            associate with GSNI
                CntXs
            referred by Usr
            Handle Address/Places

        Usr Actions
            List Cnts owned and
        '''

        pass