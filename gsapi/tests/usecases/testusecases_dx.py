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
class TestUseCaseDx(TestCase):
    # Flask sessions = {'sessionKey':val}
    def test_associate(self):
        self.associate(to_obj, from_obj)
    def test_delete(self):
        node  = getId()#getid from mongo
        parents = [] #get all parents in this list
        self.update_parents(parents)#parents is a list
        children = [] #get all children in this list
        self.update_children(children)
        self.delete_node(node)
    def test_move(self):
        self.delete_node(node)
        self.associate(to_obj, from_onj)
    def test_update_attr(self):
        print 'mark itself dirty'
        print 'if object is already dirty try after 0.5 seconds'
        print "update attribute:"
        self.update_parents(parents)
        self.update_children(children)
        print 'mark itself clean'
    def test_read_obj(self, oid):
        print 'test if object is dirty if so send a message'
        check_dirty(oid)
        read_obj(oid)
    def test_write_obj(self, oid, data):
        print 'test if object is dirty if so do not allow writing'
        check_dirty(oid)
        write_obj(oid, data)
