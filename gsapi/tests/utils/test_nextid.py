# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
import sys
from tests.base import MongoTestCase
import models
import controllers
from utils.nextid import nextId

class TestNextId(MongoTestCase):
    usrOID = "50468de92558713d84b03fd7"
    def post_sample(self, doc):
        response = controllers.Generic(self.db).post(**{'usrOID':self.usrOID, 'docs': [doc]})
        assert response['status'] == 200
        return response['response']['docs'][0]['doc']
        
    def test_nextid_id_empty_collection(self):
        '''Doc this
            '''
        db      = self.db
        generic = controllers.Generic(db)
        coll    = db['cnts']

        response = nextId(coll)

        assert response['status'] == 200
        assert response['nextId'] == 1
    def test_nextid_insert_new_record(self):
        '''Doc this
            '''
        db      = self.db
        generic = controllers.Generic(db)
        
        # lets create a some sample docs bypassing tmp process.
        sample_doc = self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'Stooge'})
        sample_doc = self.post_sample({'_c': 'Prs', 'fNam': 'Moe', 'lNam': 'Stooge'})
        
        assert sample_doc['dId'] == 2 
        
if __name__ == "__main__":
    unittest.main()
