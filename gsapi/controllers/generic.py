# -*- coding: utf-8 -*-
import os
from gsapi.extensions import validate
from bson import ObjectId
import re
import datetime
from gsapi import models

class Generic(object):
    """Docstring for class Generic"""

    def __init__(self, db, es = None):
        #: Doc comment for instance attribute db
        self.db = db
        self.es = es

    def put(self, **kwargs):
        """Docstring for put method:"""
        db = self.db
        # TODO: accomodate where clause to put changes to more than one doc.
        class_name = kwargs['class_name']
        model = getattr(models, class_name)
        collection_name = model.meta['collection']
        collection = db[collection_name]

        response = {}
        docs = []
        status = 200

        data = kwargs['data']
        usrid = kwargs['usrid']

        # expecting where
        where = data['where']
        patch = data['patch']

        # validata patch
        # init model for this doc
        patch_errors = validate(model, patch)
        if patch_errors:
            response['errors'] = patch_errors['errors']
            response['total_errors'] = patch_errors['count']
            status = 400

            return prep_response(response, status = status)

        # until we get signals working
        # manually include modified event details
        # patch['mBy'] = user_id
        patch['mBy'] = ObjectId(usrid)
        patch['mOn'] = datetime.datetime.utcnow()

        # https://github.com/mongodb/mongo-python-driver/blob/master/pymongo/collection.py#L1035
        resp = db.command('findAndModify', collection_name,
            query = where,
            update = {"$set": patch},
            new = True
        )

        response['collection'] = collection_name
        response['total_invalid'] = 0
        response['id'] = id.__str__()
        response['doc'] = resp['value']

        return {'response': response, 'status_code': status}
    
    def post(self, **kwargs):
        """Docstring for post method:"""
        db = self.db
        class_name = kwargs['class_name']
        model = getattr(models, class_name)
        collection_name = model.meta['collection']
        collection = db[collection_name]

        response = {}
        docs = []
        status = 200

        docs_to_post = kwargs['docs']

        post_errors = []
        total_errors = 0
        for doc in docs_to_post:
            errors = {}
            user_id = "50468de92558713d84b03fd7"

            # need to stuff in class_name
            doc['_c'] = class_name

            # Validate
            doc_errors = validate(model, doc)
            if doc_errors:
                total_errors += doc_errors['count']
                post_errors.append(doc_errors)
                continue

            # init model for this doc
            m = model(**doc)

            #log date time user involved with this event
            m.logit(user_id, 'post')

            # need to stuff into mongo
            doc_validated = m.to_python()
            try:
                doc_validated['_c'] = m.meta['_c']
            except:
                pass

            doc_info = {}

            id = str(collection.insert(doc_validated, safe = True))
            doc_info['id'] = id
            doc_info['doc'] = doc_validated
            #doc_info['link'] = get_document_link(class_name, id)

            docs.append(doc_info)

        response['total_inserted'] = len(docs)

        if post_errors:
            response['total_invalid'] = len(post_errors)
            response['errors'] = post_errors
            response['total_errors'] = total_errors
            status = 400
        else:
            response['total_invalid'] = 0


        response['docs'] = docs

        return {'response': response, 'status_code': status}
    
    def get(self, **kwargs):
        """Docstring for get method:"""
        db = self.db
        class_name = kwargs['class_name']
        model = getattr(models, class_name)
        collection_name = model.meta['collection']
        collection = db[collection_name]

        response = {}
        docs = []
        status = 200

        # if an id was passed, try to return only that one
        if 'id' in kwargs:
            id = kwargs['id']
            doc = collection.find_one({"_id": ObjectId(id)})
            response['doc'] = doc
            return {'response': response, 'status_code': status}



        if 'where' in kwargs:
            where = kwargs['where']
        else:
            where = {}

        # this allows us to filter results on the type of contact involved
        # contacts return all
        # persons return contacts that are persons, etc.
        where['_c'] = class_name

        fields = kwargs['fields'] if 'fields' in kwargs else None
        sort_raw = kwargs['sort'] if 'sort' in kwargs else None

        # mongo wants sorts like: [("fld1", <order>), ("fld2", <order>)]
        sorts = []
        if sort_raw:
            flds = sort_raw
            for fld in flds:
                sorts = [(k, int(v)) for k, v in fld.iteritems()]

        skip = int(kwargs['skip']) if 'skip' in kwargs else 0
        limit = int(kwargs['limit']) if 'limit' in kwargs else 0
        skip_limit = skip > -1 and limit

        if sorts:
            cursor = collection.find(spec = where, fields = fields, skip = skip, limit = limit).sort(sorts)
        else:
            cursor = collection.find(spec = where, fields = fields, skip = skip, limit = limit)
        for doc in cursor:
            docs.append(doc)

        # handle any virtual fields
        if 'vflds' in kwargs:
            vflds = kwargs['vflds']
            for i, doc in enumerate(docs):
                initialed_model = model(**doc)
                for vfld in vflds:
                    docs[i][vfld] = getattr(initialed_model, vfld)

        response['docs'] = docs

        return {'response': response, 'status_code': status}

