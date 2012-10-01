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

class TestESPyes(TestCase):
    print "ESPyes tests"
    print "============"

    def test_es_sample_data(self):
        print "\TestESPyes.test_es_sample_data"
        print """LOAD SAMPLE DOCS:\n"""

        resp = self.load_sample('contacts_es')
        assert resp['status'] == 200

        sample_docs = resp['response']['docs']

        index_name = "test-contacts"
        document_type = 'Cnt'
        es = self.es
        es.delete_index_if_exists(index_name)
        es.create_index(index_name)

        es.put_mapping(document_type, {'properties':models.esCnt}, [index_name])

        for doc in sample_docs:
            es.index({"dNam":doc['dNam'], "parsedtext":doc['dNam']}, index_name, doc['_c'], doc['_id'].__str__())

        es.default_indices = [index_name]
        q = TermQuery("dNam", "joe")
        results = es.search(query = q)
        for r in results:
            print r
            # add assert for expected result

if __name__ == "__main__":
    unittest.main()
