# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from base import TestCase

import os
import json
import urllib2
import urllib
import rawes
import pyes

class TestESPyes(TestCase):

    #by default server runs at port 9200
    URL = "http://localhost:9200/"
    ES = rawes.Elastic('localhost:9200')

    def test_index_sample_data(self):
        print "\nTestUtils.test_load_data"
        print """LOAD SAMPLE DOCS:\n"""

        from gsapi.utils import load_data

        json_fname = 'contacts'
        resp = self.load_sample(json_fname)

        print "From: {json_fname}, {count} docs loaded, {errors} errors.".format(json_fname=json_fname, count=resp['response']['total_inserted'], errors=resp['response']['total_invalid'])
        if not resp['status'] == 200:
            print resp

        assert resp['status'] == 200


    def test_elastic_server_running(self):
        response = urllib2.urlopen(self.URL)
        data = json.loads(response.read().strip())

        #check if it returns 200 and ok==true

        if data["status"] == 200 and data["ok"] == True:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_elasticsearch_put(self):
        response = self.ES.put('tweets/tweet/1', data={
            'user' : 'shiv',
            'post_date' : '2012-09-25T01:40:30',
            'message' : 'Tweeting about elasticsearch'
        })

        if response["_type"] == "tweet" and response["ok"] == True and response["_index"] == "tweets":
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_elasticsearch_get(self):
        response = self.ES.get('tweets/tweet/_search', data="""
        {
            "query" : {
		        "match_all" : {}
    	    }
        }
        """
        )

        if len(response["hits"]["hits"]) != 0:
            self.assertTrue(True)
        else:
            self.assertTrue(Flase)

    def test_elasticsearch_post(self):
        response = self.ES.post('tweets/tweet/', data={
            'user' : 'larry',
            'post_date' : '2012-09-25T09:02:01',
            'message' : 'More tweets about elasticsearch'
        })

        if response["_type"] == "tweet" and response["ok"] == True and response["_index"] == "tweets":
            self.assertTrue(True)
        else:
            self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
