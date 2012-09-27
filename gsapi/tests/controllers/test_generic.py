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
import models
import controllers
# from pprint import pprint

def pprint(varname, dat):
    print "%s = %s" % (varname, json.dumps(dat, sort_keys=True, indent=4))

class TestGeneric(TestCase):
    class_name = 'Prs'

    def test_post_one(self):
        print "## nTestGeneric.test_post_one"
        print '''### INSERT NEW PERSON:'''

        db       = self.db

        # here is the basic function call being tested
        fn = "controllers.generic.get(db, **args)"

        # POST ONE ################################
        host = self.host
        sample_doc = {
            "fNam":"johnathan",
            "lNam":"doe",
            # "mOn": {"$date": 1347893866298},
            "mOn": isodate.parse_datetime("2012-09-27T21:43:33.927Z"),
            "dOn": isodate.parse_datetime("2012-09-29T21:43:33.927Z"),
            "oBy": ObjectId("50468de92558713d84b03fd0"),
            "rBy": ObjectId("50468de92558713d84b03fd7"),
            "gen":'m',
            "emails" : [{
                "email" : "john@doe.com"
            }]
        }

        args               = {}
        args['class_name'] = self.class_name
        args['docs']       = [sample_doc]

        print
        print "POST ONE doc:"
        print "CALL:\n" + fn + "\nWITH:"
        print 'args =', args
        print

        response = controllers.generic.post(db, **args)

        assert response['status_code'] == 200
        data     = response['response']
        got_docs = data['docs']


        assert data['total_inserted'] == 1

        doc = data['docs'][0]['doc']
        id  = data['docs'][0]['id']
        print "INSERTED OBJECT_ID:", id
        assert doc['fNam'] == sample_doc['fNam']














    def test_get(self):
        print "\nTestGeneric.test_get"
        print """LOAD SAMPLE DOCS:\n"""

        db       = self.db
        response = self.load_sample('contacts')
        assert response['status'] == 200

        sample_docs = response['response']['docs']
        # grab a random doc from sample docs
        sample_doc_offset        = randint(0, len(sample_docs)-1)
        sample_doc               = sample_docs[sample_doc_offset]
        sample_doc_id            = sample_doc['_id']

        # here is the basic function call being tested
        fn = "controllers.generic.get(db, **args)"

        # I have all these if doit: so that I can code-fold and/or switch off
        doit = 0
        if doit: # ALL ################################
            test_expected_count = 4 # Note the filter on _c

            args = {'class_name': self.class_name}

            print
            print "GET ALL docs:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200
            data     = response['response']
            got_docs = data['docs']

            assert test_expected_count == len(got_docs)
            print "Successfully returned %d sample docs." % len(got_docs)
        if doit: # VIRTUAL FIELDS ################################
            vflds              = ["dNam"]
            args               = {}
            args['class_name'] = self.class_name
            args['vflds']      = json.dumps(vflds)

            print
            print "VIRTUAL FIELDS:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            print "Verify virtual field was returned with result. "
            assert vflds[0] in got_docs[0]
            print "Success"
        if doit: # ONE BY ID ################################
            args               = {}
            args['class_name'] = self.class_name
            args['id']         = sample_doc_id.__str__()

            print
            print "ONE BY ID:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_doc = data['doc']

            assert sample_doc['_id'] == got_doc['_id']
            print 'Success'
        if doit: # WHERE by fNam ################################
            test_expected_count= 1
            where_test         = {"fNam":"sue"}
            args               = {}
            args['class_name'] = self.class_name
            args['where']      = json.dumps(where_test)

            print
            print "WHERE by fNam:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            print "Success. Expected %d docs and found %d docs" % (test_expected_count, len(got_docs))
            assert len(got_docs) == test_expected_count
            print 'Success'
        if doit: # WHERE by datetime ################################
            test_field          = 'mOn'
            test_value          = 1347644492400
            test_expected_count = 1
            where_test          = {test_field:{"$date":test_value}}
            args                = {}
            args['class_name']  = self.class_name
            args['where']       = json.dumps(where_test)

            print
            print "WHERE by datetime:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            print "Success. Expected %d docs and found %d docs" % (test_expected_count, len(got_docs))
            assert len(got_docs) == test_expected_count
            print 'Success'
        if doit: # WHERE by ObjectId ################################
            test_field          = 'mBy'
            test_value          = "50468de92558713d84b03ed7"
            where_test          = {test_field:{"$oid":test_value}}
            args                = {}
            args['class_name']  = self.class_name
            args['where']       = json.dumps(where_test)
            test_expected_count = 1

            print
            print "WHERE by ObjectId:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            print "Success. Expected %d docs and found %d docs" % (test_expected_count, len(got_docs))
            assert len(got_docs) == test_expected_count
            print 'Success'
        if doit: # SORT ################################
            test_field          = 'fNam'
            sort_test           = {'fld':test_field, 'values':['nam1','nam2']}
            # sort                = [{test_field:"1"}]
            sort                = [{test_field: 1}]
            args                = {}
            args['class_name']  = self.class_name
            args['sort']        = json.dumps(sort)

            print
            print "SORT:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            sort_values = sort_test['values']
            for i in range(len(sort_test['values'])):
                assert got_docs[i][sort_test['fld']] == sort_values[i]
            print 'Success'
        if doit: # FIELDS LIST ################################
            fields              = ["fNam", "title"]
            args                = {}
            args['class_name']  = self.class_name
            args['fields']      = json.dumps(fields)

            print
            print "FIELDS LIST:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            assert fields == got_docs[0].keys()[1:]
            print 'Success'
        if doit: # SKIP & LIMIT ################################
            skip = 1
            limit = 1
            args                = {}
            args['class_name']  = self.class_name
            args['skip']      = json.dumps(skip)
            args['limit']      = json.dumps(limit)

            print
            print "SKIP & LIMIT:"
            print "CALL:\n" + fn + "\nWITH:"
            pprint('args', args)
            print

            response = controllers.generic.get(db, **args)

            assert response['status_code'] == 200

            data     = response['response']
            got_docs = data['docs']

            assert len(got_docs) == limit
            print "Success. Expected %d docs and found %d docs" % (limit, len(got_docs))

if __name__ == "__main__":
    unittest.main()
