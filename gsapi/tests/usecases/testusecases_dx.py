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
class TestUseCaseUsr(TestCase):
    # Flask sessions = {'sessionKey':val}
    def createDx(self, to_obj, from_obj):
        pass
    def createDxRel(self, to_obj, from_obj):
        pass
    def associate(self, to_obj, from_onj):
        self.createDx()
        self.createDxRel()
    def test_associate(self):
        self.associate(to_obj, from_obj)
    def update_parents(self, parents):
        print "Update immediate parent"
        pass
    def update_children(self, children):
        print "Update children recursively:"
        pass
    def delete_node(self, node):
        pass
    def getId(self):
        pass
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
    def update_attr(self):
        print "update attribute:"
        self.update_parents(parents)
        self.update_children(children)