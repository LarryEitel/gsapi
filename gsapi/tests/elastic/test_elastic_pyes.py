# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase

import os
import json
from pyes import TermQuery
import models
import time
import datetime

class TestESPyes(TestCase):
    print "ESPyes tests"
    print "============"

    def test_es_sample_data(self):
        print "\TestESPyes.test_es_sample_data"
        print """LOAD SAMPLE DOCS:\n"""

        resp = self.load_sample('contacts_es')
        assert resp['status'] == 200

        sample_docs = resp['response']['docs']

        document_type = 'Cnt'
        es = self.es
        index_name = es.__dict__['index_name']
        es.delete_index_if_exists(index_name)
        es.create_index(index_name)

        es.put_mapping(document_type, {'properties':models.esCnt}, [index_name])


        for doc in sample_docs:
            es.index({"dNam":doc['dNam'],
                "oOn": doc['oOn'],
                "title": doc['title'],
                "parsedtext":doc['dNam']},
                index_name,
                doc['_c'], doc['_id'].__str__())


        es.default_indices = [index_name]
        # es.refresh(index_name)
        time.sleep(1)
        q = TermQuery("title", "dr")
        results = es.search(query = q)
        for r in results:
            assert r.title == 'Dr'

        q = TermQuery("oOn", datetime.datetime(2012, 10, 8, 13, 44, 33, 851000))
        results = es.search(query = q)
        for r in results:
            assert r.dNam == 'Einstein, Mr Larry Wayne'


if __name__ == "__main__":
    unittest.main()
