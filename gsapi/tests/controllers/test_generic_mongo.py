# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
import sys
from tests.base import MongoTestCase
import json
import time
import isodate
import yaml
from random import randint
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import models
import controllers
#from utils import appG, sessionG
from models.extensions import validate, validate_partial, doc_remove_empty_keys
from schematics.serialize import to_python

class TestGenericMongo(MongoTestCase):
    print "Generic tests"
    print "=============="
    usrOID = "50468de92558713d84b03fd7"
    usr    = {"OID": "50468de92558713d84b03fd7"}
    def post_sample(self, doc):
        response = controllers.Generic(self.usr, self.db).post(**{'usrOID':self.usrOID, 'docs': [doc]})
        assert response['status'] == 200
        return response['response']['docs'][0]['doc']
    def test_post_attr(self):
        '''Post a new item to a listType attribute/field
            '''
        db      = self.db
        generic = controllers.Generic(self.usr, db)

        # lets create a some sample docs bypassing tmp process.
        sample_doc = self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'Stooge'})
        generic.post_attr(sample_doc, 'emails', 'Email', {'typ': 'work', '_c': 'Email', 'address': 'bill@ms.com', 'prim': '1'}, useTmpDoc=False)
        generic.post_attr(sample_doc, 'emails', 'Email', {'typ': 'home', '_c': 'Email', 'address': 'steve@apple.com'}, useTmpDoc=False)
        posted_to_doc = db['cnts'].find_one({'_id': sample_doc['_id']})
        
        # should now have 2 emails
        assert len(posted_to_doc['emails']) == 2


    def test_post_listtype(self):
        '''Passing in doc with OID should clone the doc and save in tmp collection. Set isTmp = True.
            '''
        db      = self.db
        generic = controllers.Generic(self.usr, db)

        # lets create a some sample docs bypassing tmp process.
        sample_doc = self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'Stooge'})



        # now let's pretent to initiate an update of this doc
        response = generic.post(**{'usrOID': "50468de92558713d84b03fd7", 'docs': [sample_doc]})
        
        # now let's add emails
        test_field   = 'emails'
        test_field_c = 'Email'
        test_value   = [{'typ': 'work', '_c': 'Email', 'address': 'bill@ms.com', 'prim': '1'},
                        {'typ': 'home', '_c': 'Email', 'address': 'steve@apple.com', 'note': 'Deceased'}]
        doc = {
            '_c'     : sample_doc['_c'],
            '_id'    : sample_doc['_id'],
            'attrNam': test_field,
            'attr_c' : test_field_c,
            'attrVal': test_value,
            }

        response = generic.post(**{'usrOID': "50468de92558713d84b03fd7", 'docs': [doc]})

        assert response['status'] == 200
        
        # let's get the tmp doc
        tmp_doc_id           = doc['_id']
        tmp_doc              = db['cnts_tmp'].find_one({'_id': ObjectId(tmp_doc_id)})
        
        # should have the correct number of added attr elements
        assert len(test_value) == len(tmp_doc[test_field])

        # let's submit changes to original source doc.
        response = generic.post(**{'usrOID': self.usrOID, 'docs': [tmp_doc]})
        doc      = response['response']['docs'][0]['doc']

        # original doc should now have updated value
        assert doc[test_field][0]['address'] == test_value[0]['address']
        
        # verify that eIds was correctly added
        assert doc['eIds']['emails'] == 3
        


    def test_put_listtype(self):
        '''Need doc here
            '''
        db       = self.db
        generic  = controllers.Generic(self.usr, db)

        # lets create a some sample docs bypassing tmp process.
        sample_docs = [
            self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'Stooge'}),
            self.post_sample({'_c': 'Prs', 'fNam': 'Moe', 'lNam': 'Stooge'}),
            self.post_sample({'_c': 'Prs', 'fNam': 'Curley', 'lNam': 'Stooge', "emails" : [{
                      "prim" : True,
                      "dNam" : "typ_work: bill@ms.com(Primary)",
                      "eId" : 1,
                      "address" : "bill@ms.com",
                      "typ" : "work",
                      "slug" : "typ_work:_bill@ms.com(primary)",
                      "dNamS" : "typ_work:_bill@ms.com(primary)",
                      "_c" : "Email"
                    }, {
                      "dNam" : "typ_home: steve@apple.com",
                      "eId" : 2,
                      "address" : "steve@apple.com",
                      "typ" : "home",
                      "slug" : "typ_home:_steve@apple.com",
                      "dNamS" : "typ_home:_steve@apple.com",
                      "_c" : "Email"
                    }]}),
            ]

        # grab a random doc from sample docs
        sample_doc        = sample_docs[2]
        sample_doc_id     = sample_doc['_id']

        # when we need to edit most docs, we lock the doc and clone a tmp doc to work on.
        # now let's pretent to initiate an update of this doc
        response = generic.post(**{'usrOID': self.usrOID, 'docs': [sample_doc]})
        
        # this is the temp doc, the original is locked
        doc_tmp           = response['response']['docs'][0]['doc']
        

        test_field        = 'emails'
        test_value        = [{
                "_c"     : "Email",
                "eId"    : 2,
                "address": "fred@apple.com",
                "typ"    : "home",
                "w"      : 0.0
            }]
        test_eId          = 2
        test_elemOffset   = 1
        data              = {
                "_c"   : sample_doc['_c'],
                'where': {'_id': sample_doc['_id'], test_field + '.eId': test_eId},
                'patch': {
                        test_field: test_value,
                    },
                "eId"  : 2
                }
        
        # submit patch to tmp doc
        response = generic.put(**{'usrOID': ObjectId(self.usrOID), 'data': data})
        tmp_doc  = response['response']['doc']
        
        # let's submit changes to original source doc.
        response = generic.post(**{'usrOID': self.usrOID, 'docs': [tmp_doc]})
        doc      = response['response']['docs'][0]['doc']

        # original doc should now have updated value
        assert doc[test_field][test_elemOffset]['address'] == test_value[0]['address']
        

    def test_put(self):
        '''Need doc here
            '''
        db       = self.db
        generic  = controllers.Generic(self.usr, db)

        # lets create a some sample docs bypassing tmp process.
        sample_docs = [
            self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'Stooge'}),
            self.post_sample({'_c': 'Prs', 'fNam': 'Moe', 'lNam': 'Stooge'}),
            self.post_sample({'_c': 'Prs', 'fNam': 'Curley', 'lNam': 'Stooge'}),
            ]
        
        # grab a random doc from sample docs
        sample_doc_offset = randint(0, len(sample_docs) - 1)
        sample_doc        = sample_docs[sample_doc_offset]
        sample_doc_id     = sample_doc['_id']

        # when we need to edit most docs, we lock the doc and clone a tmp doc to work on.
        # now let's pretent to initiate an update of this doc
        response = generic.post(**{'usrOID': self.usrOID, 'docs': [sample_doc]})
        
        # this is the temp doc, the original is locked
        doc_tmp           = response['response']['docs'][0]['doc']

        test_field        = 'fNam'
        test_value        = 'longname'
        data = {
                "_c"   : sample_doc['_c'],
                'where': {'_id': sample_doc['_id']},
                'patch': {
                        test_field: test_value,
                        "rBy"     : ObjectId(self.usrOID)
                    }
                }
        
        response = generic.put(**{'usrOID': ObjectId(self.usrOID), 'data': data})
        doc      = response['response']['doc']
        
        
        # did it properly update the value?
        assert doc[test_field] == test_value
        
        # let's submit changes to original source doc.
        response = generic.post(**{'usrOID': self.usrOID, 'docs': [doc]})
        doc      = response['response']['docs'][0]['doc']

        # original doc should now have updated value
        assert doc[test_field] == test_value
    def test_post_new(self):
        '''Passing in doc with only _c(lass) should initialize a doc and save in tmp collection.
            '''
        sample_doc = self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'King', 'suffix': 'Sr'})
    def test_post_update(self):
        '''Passing in doc with OID should clone the doc and save in tmp collection. Set isTmp = True.
            '''
        db      = self.db
        generic = controllers.Generic(self.usr, db)
        
        # lets create a sample doc bypassing tmp process.
        doc = self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'King', 'suffix': 'Sr'})

        # now let's pretent to initiate an update of this doc
        args                 = {}
        args['usrOID']       = self.usrOID
        
        sample_doc           = doc
        args['docs']         = [sample_doc]
        
        response             = generic.post(**args)
        
        # let's get the sample source doc that should now have a cloned copy inserted into the tmp collection
        src_doc_id           = doc['_id']
        src_doc              = db['cnts'].find_one({'_id': ObjectId(src_doc_id)})
        
        # should be locked
        assert src_doc['locked']
        
        assert response['status'] == 200
        data     = response['response']
        
        assert data['total_inserted'] == 1
        tmp_doc = data['docs'][0]['doc']
        
        # _id's should match
        assert src_doc['_id'] == tmp_doc['_id']
        
        # should be flagged as tmp
        assert tmp_doc['isTmp']
    def test_post_submit(self):
        '''Passing in doc with OI and isTmp is set will move/clone the tmp doc into the base/primary doc collection and remove the tmp doc.
            '''
        db      = self.db
        generic = controllers.Generic(self.usr, db)

        # lets create a sample doc bypassing tmp process.
        doc = self.post_sample({'_c': 'Prs', 'fNam': 'Larry', 'lNam': 'King', 'suffix': 'Sr'})
        
        # now let's pretent to initiate an update of this doc
        args                 = {}
        args['usrOID']       = self.usrOID
        
        args['docs']         = [doc]
        
        response             = generic.post(**args)
        
        # let's get the tmp doc
        src_doc_id           = doc['_id']
        tmp_doc              = db['cnts_tmp'].find_one({'_id': ObjectId(src_doc_id)})
        
        # UI will handle making changes to specific fields.
        # Let's make a sample change to the tmp doc.
        # NOTE: THIS IS A NO-NO.
        tmp_doc = db['cnts_tmp'].find_and_modify(
            query = {'_id': tmp_doc['_id']},
            update = {"$set": {'fNam2': 'Wayne'}},
            new = True
        )                   
        
        # Once any updates are made to tmp/clone copy, update original/source doc. Then delete the temp doc.

        args                 = {}
        args['usrOID']       = self.usrOID
        args['docs']         = [tmp_doc]
        
        response             = generic.post(**args)
        
        assert response['status'] == 200

        # let's get the sample source doc that should now have been updated from the tmp copy
        src_doc              = db['cnts'].find_one({'_id': ObjectId(src_doc_id)})
        
        # should not be locked
        assert not src_doc['locked']
        
        # should have the sample change
        assert src_doc['fNam2'] == 'Wayne'
        
        # tmp doc should have been removed
        assert not db['cnts_tmp'].find_one({'_id': ObjectId(src_doc_id)})  


if __name__ == "__main__":
    unittest.main()
