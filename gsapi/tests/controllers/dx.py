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

class Dx(models):
	def write_obj(self, oid, data):
		oid.attrs = data
	def read_obj(self, oid):
		return oid.attrs
	def check_dirty(self, oid):
		return oid.dirty
	def mark_dirty(self, objs[]):
		obj.dirty = 1
		print 'mark alll dirty'
	def mark_clean(self, objs[]):
		obj.dirty = 0
		ptint 'mark all clean'
    def createDx(self, to_obj, from_obj):
    	print 'mark all three object to_obj, from_obj, dx_obj dirty'
    	dx_obj = Dx()
    	self.mark_dirty([to_obj, from_obj, dx_obj])
    	print 'if objects are already dirty try after .5 seconds'
        pass
    def createDxRel(self, to_obj, from_obj):
    	print 'mark all three object to_obj, from_obj, dxRel_obj dirty'
    	dxRel_obj = DxRel()
    	self.mark_dirty([to_obj, from_obj, dxRel_obj])
    	print 'if objects are already dirty try after .5 seconds'
        pass
    def associate(self, to_obj, from_onj):
        self.createDx()
        self.createDxRel()
        print 'mark all four object to_obj, from_obj, dx_obj clean'
        print 'if objects are already dirty try after .5 seconds'
    def update_parents(self, parents):
    	print 'mark all parents dirty'
    	print 'Iterate over obj.tos[dRel.ids[]] to get immediate parents oids'
        print "Update immediate parent"
        print 'mark all parents clean'
        pass
    def update_children(self, children):
    	print 'mark all children dirty'
        print "Update children recursively:"
        print 'Iterate over obj.froms[dRel.ids[]] to get immediate children oids'
        print 'mark all children clean'
        pass
    def delete_node(self, node):
        pass
    def getId(self):
        pass