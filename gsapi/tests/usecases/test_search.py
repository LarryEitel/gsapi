# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase
from gsapi.utils import mongo_json_object_hook

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
class TestUseCaseSearch(TestCase):
	def test_search_oid(self, oid):
		print 'search elastic for that oid'
		#Therefore oid should be one index
		elasticsearch_oid(oid)
	def test_search_fName(self, fName):
		print 'search elastic for that fName among persons'
		#an index based on fNames should be created
		elasticsearch_fName(fName)
	def test_search_lName(self, lName):
		print 'search elastic for that lName among persons'
		#an index based on lNames should be created
		elasticsearch_lName(lName)
	def test_search_rel(self, dNam, rel):
		print 'search elastic given a dName and relation'