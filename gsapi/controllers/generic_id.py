# -*- coding: utf-8 -*-
import os
from gsapi.extensions import validate
from bson import ObjectId
import re
import datetime
from gsapi import models
from gsapi.controllers.generic import Generic

class GenericId(Generic):
    """Docstring for class Generic"""

    def nextId(self, _c):
        '''looking for max id for given class _c'''
        db                 = self.db
        ids                = db['ids']
        
        response           = {}
        response['status'] = 200

        # find max id
        # insure index db[collection].ensureindex({['_c':1], ['id', -1]})
        try:
            doc = ids.find_one({'_c': _c})
            if not doc:
                nextId = 1
            else:
                nextId = int(doc['id']) + 1
        except:
            response['error']  = 'Unable to query for max id.'
            response['status'] = 400
            return {'response': response, 'status_code': status}

        maxTries = 5
        tries    = 0
        while True:
            # try to insert a doc into ids collection with nextId
            # if it fails, it is likely because someone was able to insert nextId be I was.
            try:
                retVal             = ids.insert({'_c': _c, 'id': nextId})
                response['nextId'] = nextId
                break

            # may need to watch for type of error
            # value exits, dup key error
            except:
                # if error is because of existing value
                nextId += 1

                # # if other error and tries < maxTries
                # errorCode = 1000
                # if errorCode == 1000
                #     if tries < maxTries:
                #         # try again
                #         tries += 1
                #     else:
                #         # otherwise
                #         response['error']  = 'Error ___ reached maxTries.'
                #         response['status'] = 400
                #         break

        return {'response': response, 'status_code': status}
