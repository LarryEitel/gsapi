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
class TestUseCaseUsr(TestCase):
    # Flask sessions = {'sessionKey':val}
    def test_one(self):
        print "\n\nTestUseCaseUsr.test_one\n"

        print "HTTPS for pw:"
        print "CREATE Usr:"
        print "LOGIN Usr:"
        # return a session value

        print "RESET Password:"
        print "FORGOT Password:"

        # these require email service running
        print "FORGOT UserId:"
        print "VALIDATION Email:"
        print "CHANGE Primary Email:"
    
    def crete_company(self):
        print "create one company:"
