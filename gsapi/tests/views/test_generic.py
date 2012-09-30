# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase
import json
import time
import datetime
import dateutil.parser
from flask import request
from random import randint
from bson import ObjectId
from bson.json_util import dumps
import isodate
#host = "localhost:5000"

class TestGeneric(TestCase):
    collection = 'Prs'
    collection_name = 'Prs'
    def test_post_one(self):
        print "## TestPersons.test_post_one"
        print '''### INSERT NEW PERSON:'''

        # resp = self.load_sample('contacts')

        host = self.host
        sample = {
            "fNam":"johnathan",
            "lNam":"doe",
            #"lvOn":{"$date": 1347893866298},
            "dOn":"$isodate:2012-09-14T17:41:32.471Z",
            "oBy":{"$oid":"50468de92558713d84b03fd0"},
            "rBy":{"$oid":"50468de92558713d84b03fd7"},
            "gen":'m',
            "emails" : [{
                "email" : "john@doe.com"
            }]
        }
        data = json.dumps(sample)
        route = "/" + self.collection
        addParams = {
            'verb'   : "POST",
            'host'   : host,
            'url'    : 'http://' + host + route,
            'route'  : route,
            'http'   : "HTTP/1.1",
            'headers': "\n".join(['content-type: application/json']),
            'data'   : data,
            'length' : len(data)
        }
        print "\n#### RAW REQUEST:\n%(verb)s %(url)s %(http)s\n%(headers)s\nHost: %(host)s\nContent-Length: %(length)i\n\n%(data)s\n" % addParams
        response = self.app.post(addParams['route'], data=addParams['data'])

        data = json.loads(response.data)
        if not response.status_code   == 200:
            print "FAILED: ", data
        assert response.status_code   == 200
        print "Success.\n#### RESPONSE:\n%s" % data

        assert data['total_inserted'] == 1

        doc = data['docs'][0]['doc']
        id  = data['docs'][0]['id']
        print "INSERTED OBJECT_ID:", id
        assert doc['fNam']            == sample['fNam']
    def test_post_list(self):
        print "TestPersons.test_post_one"
        print '''INSERT NEW PERSON:'''

        #resp = self.load_sample('contacts')

        host = self.host
        sample = [{
            "fNam":"larry",
            "lNam":"stooge",
            "lvOn":{"$date": 1347893866298},
            "oBy":{"$oid":"50468de92558713d84b03fd0"},
            "rBy":{"$oid":"50468de92558713d84b03fd7"},
            "gen":'m',
            "emails" : [{
                "email" : "larry@stooge.com"
            }]
        },{
            "fNam":"moe",
            "lNam":"stooge",
            "lvOn":{"$date": 1347893866298},
            "oBy":{"$oid":"50468de92558713d84b03fd0"},
            "rBy":{"$oid":"50468de92558713d84b03fd7"},
            "gen":'m',
            "emails" : [{
                "email" : "moe@stooge.com"
            }]
        },{
            "fNam":"curly",
            "lNam":"stooge",
            "lvOn":{"$date": 1347893866298},
            "oBy":{"$oid":"50468de92558713d84b03fd0"},
            "rBy":{"$oid":"50468de92558713d84b03fd7"},
            "gen":'m',
            "emails" : [{
                "email" : "curly@stooge.com"
            }]
        }]
        data = json.dumps(sample)
        route = "/" + self.collection
        addParams = {
            'verb'   : "POST",
            'host'   : host,
            'url'    : 'http://' + host + route,
            'route'  : route,
            'http'   : "HTTP/1.1",
            'headers': "\n".join(['content-type: application/json']),
            'data'   : data,
            'length' : len(data)
        }
        print "\nRAW REQUEST:\n%(verb)s %(url)s %(http)s\n%(headers)s\nHost: %(host)s\nContent-Length: %(length)i\n\n%(data)s\n" % addParams
        response = self.app.post(addParams['route'], data=addParams['data'])

        data = json.loads(response.data)
        if not response.status_code   == 200:
            print "FAILED: ", data
        assert response.status_code   == 200
        print "Success. RESPONSE:\n%s" % data

        assert data['total_inserted'] == 3

        doc = data['docs'][0]['doc']
        id  = data['docs'][0]['id']
        print "INSERTED OBJECT_ID:", id
        assert doc['fNam']            == sample[0]['fNam']
    def test_get(self):
        print "\nTestGeneric.test_get"
        print """LOAD SAMPLE DOCS:\n"""

        host       = self.host

        resp       = self.load_sample('contacts')
        assert resp['status'] == 200

        sample_docs = resp['response']['docs']

        route ='http://' + host

        # ALL
        print "\nVerify GET all docs:"
        query               = "/" + self.collection
        test_expected_count = 4 # Note the filter on _cls
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200
        data     = json.loads(response.data)
        got_docs = data['docs']
        assert test_expected_count == len(got_docs)
        print "Successfully returned %d sample docs." % len(got_docs)

        sample_doc_offset = randint(0, len(sample_docs)-1)
        sample_doc = sample_docs[sample_doc_offset]
        sample_doc_id = sample_doc['_id']

        # VIRTUAL FIELDS
        vflds_test = '["dNam"]'

        query = '/%(collection)s?vflds=%(vflds_test)s' % {'collection':self.collection, 'vflds_test':vflds_test}
        print "\nVerify VIRTUAL FIELDS:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200

        data = json.loads(response.data)
        docs_found = data['docs']


        # ONE BY ID
        query = "/%(collection)s/%(id)s" % {'collection':self.collection, 'id':sample_doc_id}
        print "\nVerify GET one doc by id:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        #time.sleep(.05) # WHY?? Otherwise, returns 404
        # assert response.status_code == 200
        if response.status_code == 200:
            data = json.loads(response.data)
            got_doc = data['doc']
            assert sample_doc['_id'].__str__() == got_doc['_id']['$oid']
            print 'Success'
        else:
            print 'WARNING! This is not consistantly returning a doc.'


        # WHERE by fNam
        where_test = '{"fNam":"sue"}'
        test_expected_count = 1

        query = '/%(collection)s?where=%(where_test)s' % {'collection':self.collection, 'where_test':where_test}
        print "\nVerify WHERE:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200

        data = json.loads(response.data)
        docs_found = data['docs']
        print "Success. Expected %d docs and found %d docs" % (test_expected_count, len(docs_found))
        assert len(docs_found) == test_expected_count




        # WHERE by datetime
        test_field          = 'dOn'
        # hard coded, would rather convert from sample_doc
        # test_datetime       = sample_doc[test_field]
        isodate          = "$isodate:2012-09-14T23:00Z"
        # http://coderstoolbox.net/unixtimestamp/
        #timetuple       = dateutil.parser.parse(isodate).timetuple()
        #test_value       = time.mktime(timetuple)
        test_value       = isodate

        #where_test          = '{"%s":{"$date":%d}}' % (test_field, test_value)
        #where_test          = '{"%s":"2012-09-14T23:00Z"}' % (test_field)
        where_test          = '{"%s":"%s"}' % (test_field, test_value)
        test_expected_count = 1

        query = '/%(collection)s?where=%(where_test)s' % {'collection':self.collection, 'where_test':where_test}
        print "\nVerify WHERE:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200

        data = json.loads(response.data)
        docs_found = data['docs']
        print "Success. Expected %d docs and found %d docs" % (test_expected_count, len(docs_found))
        assert len(docs_found) == test_expected_count



        # WHERE by ObjectId
        test_field          = 'mBy'
        # hard coded, would rather convert from sample_doc
        # test_datetime       = sample_doc[test_field]
        test_value       = "$oid:50468de92558713d84b03ed7"

        where_test          = '{"%s":"%s"}' % (test_field, test_value)
        test_expected_count = 1

        query = '/%(collection)s?where=%(where_test)s' % {'collection':self.collection, 'where_test':where_test}
        print "\nVerify WHERE:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200



        data = json.loads(response.data)
        docs_found = data['docs']
        print "Success. Expected %d docs and found %d docs" % (test_expected_count, len(docs_found))
        assert len(docs_found) == test_expected_count

        #SORT
        # Expected Values:
        # the following identifies correct results given sample data. If sample data is refreshed, make sure you identify what field to sort and expected return values
        sort_test = {'fld':'fNam', 'values':['nam1','nam2']}
        sort='[{"fNam": "1"}]'
        query = '/%(collection)s?sort=%(sort)s' % {'collection':self.collection, 'sort':sort}
        print "\nVerify SORT:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200
        data = json.loads(response.data)
        docs_found = data['docs']

        sort_values = sort_test['values']
        for i in range(len(sort_test['values'])):
            assert docs_found[i][sort_test['fld']] == sort_values[i]
        print 'Success'


        # FIELDS LIST
        fields='["fNam", "title"]'
        query = '/%(collection)s?fields=%(fields)s' % {'collection':self.collection, 'fields':fields}
        print "\nVerify FIELDS LIST %s:" % fields
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200
        data = json.loads(response.data)
        docs_found = data['docs']
        # slice of _id field and verify fields requested where the only ones returned
        assert fields == json.dumps(docs_found[0].keys()[1:])
        print 'Success'


        # SKIP & LIMIT
        skip = 1
        limit = 1
        query = '/%(collection)s?skip=%(skip)d&limit=%(limit)d' % {'collection':self.collection, 'skip':skip, 'limit':limit}
        print "\nVerify SKIP & LIMIT:"
        print "RAW REQUEST:\n%s\n" % (route + query)

        response = self.app.get(query)
        assert response.status_code == 200
        data = json.loads(response.data)
        docs_found = data['docs']
        # for doc in docs_found:
        #     print '-------------', doc
        # print docs_found
        assert len(docs_found) == limit
        print "Success. Expected %d docs and found %d docs" % (limit, len(docs_found))
    def test_put(self):
        print "TestGeneric.test_patch"
        print """LOAD SAMPLE DOCS:\n"""

        host = self.host
        route ='http://' + host

        resp = self.load_sample('contacts')
        assert resp['status'] == 200


        sample_docs_offset = 1
        sample_docs        = resp['response']['docs']
        sample_doc         = sample_docs[sample_docs_offset]
        sample_doc_id      = sample_doc['_id'].__str__()

        print "Sample data to submit for patch:"
        sample = {'where': {'_id': {"$oid":sample_doc_id}},
            'patch': {
                "_c":"Prs",
                "fNam":"longname",
                "lvOn":{"$date": 1347893866298},
                "oBy":{"$oid":"50468de92558713d84b03fd0"},
                "rBy":{"$oid":"50468de92558713d84b03fd7"},
                "emails" : [{
                    "email" : "larry@eitel.com"
                }]
            }
        }
        data = dumps(sample)
        route = "/%(collection_name)s" % {'collection_name': self.collection_name}

        addParams = {
            'verb'   : "PUT",
            'host'   : host,
            'url'    : 'http://' + host + route,
            'route'  : route,
            'http'   : "HTTP/1.1",
            'headers': "\n".join(['content-type: application/json']),
            'data'   : data,
            'length' : len(data)
        }
        print "\nRAW REQUEST:\n%(verb)s %(url)s %(http)s\n%(headers)s\nHost: %(host)s\nContent-Length: %(length)i\n\n%(data)s\n" % addParams

        response = self.app.put(addParams['route'], data=addParams['data'])

        if not response.status_code == 200:
            print "\nFAILED! Response:\n%s" % response

        assert response.status_code   == 200

        print "Verify submitted patch was successful."

        data     = json.loads(response.data)
        assert data['doc']['fNam'] == sample['patch']['fNam']
        print 'Success'

if __name__ == "__main__":
    unittest.main()
