# -*- coding: utf-8 -*-
import os
import re
import datetime
from bson import ObjectId
import models
from models.extensions import validate
from models.logit import logit
from utils.nextid import nextId
from utils.slugify import slugify

class Generic(object):

    def __init__(self, db, es = None):
        #: Doc comment for instance attribute db
        self.db = db
        self.es = es
    
    def post(self, **kwargs):
        db           = self.db
        
        response     = {}
        docs         = []
        status       = 200
        
        usrOID       = kwargs['usrOID']
        docs_to_post = kwargs['docs']
        
        post_errors  = []
        total_errors = 0

        for doc in docs_to_post:
            errors     = {}
            
            _c         = doc['_c']
            modelClass = getattr(models, _c)

            # if _ id is passed,  it directs that a temp doc be initialized and inserted into the appropriate Tmp (temp) collection.
            # if an _id IS passed, it directs that the doc passed in be validated and inserted in the base collection and the temp doc in the temp collection be deleted.
            useTmpDoc   = not '_id' in doc.keys()
            _id         = doc['_id'] if not useTmpDoc else None
            collNam     = modelClass.meta['collection']
            collTmp     = db[collNam + '_tmp']
            coll        = db[collNam]
            
            # init model instance
            model       = modelClass(**doc)
            
            # set isTemp
            model.isTmp = useTmpDoc and 'isTmp' in model._fields

            # try to generate dNam
            # if there is a vNam class property 
            # if already has a value, use it
            if hasattr(model, 'vNam') and not useTmpDoc and 'dNam' in model._fields and not model.dNam:
                model.dNam = model.vNam

            # assign dId
            if 'dId' in model._fields and not model.dId:
                model.dId = nextId(coll)

            # generate a slug if:
            # not a temp doc and slug is empty
            if 'slug' in model._fields and not useTmpDoc and not model.slug:
                model.slug = slugify(model.dNam, coll)

            # set dNamS if used:
            # not a temp doc and dNamS is empty, set to value of slug
            if 'dNamS' in model._fields and not useTmpDoc and not model.dNamS:
                model.dNamS = model.slug

            # do not validate if using temp doc
            if not useTmpDoc:
                doc_errors = validate(modelClass, doc)
                
                if doc_errors:
                    total_errors += doc_errors['count']
                    post_errors.append(doc_errors)
                    continue

            # modelClass stuffed in all available fields
            # let's remove all empty fields to keep mongo clean.
            doc             = model.to_python()

            # do not log if using temp doc
            #log date time user involved with this event
            if not useTmpDoc:
                doc = logit(usrOID, doc, 'post')

            doc_clean       = {}
            doc_clean['_c'] = _c
            for k, v in doc.iteritems():
                if doc[k]:
                    doc_clean[k] = doc[k]
            
            doc_info = {}
            
            # posting an existing temp doc to base collection
            if _id:
                doc_clean['_id'] = str(_id)
                id = str(coll.insert(doc_clean))
                # TODO properly handle exception
                try:
                    collTmp.remove({'_id': _id})
                except:
                    pass

            # posting initialized temp doc
            else:
                # TODO properly handle exception
                try:
                    coll.insert(doc_clean)
                except:
                    pass                  
                    
            doc_info['doc']   = doc_clean
            
            # TODO
            # should return a link to object according to good practice
            #doc_info['link'] = get_document_link(class_name, id)

            docs.append(doc_info)

        response['total_inserted'] = len(docs)

        if post_errors:
            response['total_invalid'] = len(post_errors)
            response['errors']        = post_errors
            response['total_errors']  = total_errors
            status                    = 400
        else:
            response['total_invalid'] = 0

        response['docs'] = docs

        return {'response': response, 'status_code': status}
    
    def put(self, **kwargs):
        """Docstring for put method:"""
        db = self.db
        # TODO: accomodate where clause to put changes to more than one doc.
        modelClass = getattr(models, class_name)
        collNam    = kwargs['collNam'] if 'collNam' in kwargs.keys() else modelClass.meta['collection']
        collection = db[collNam]

        response = {}
        docs = []
        status = 200

        data = kwargs['data']
        usrid = kwargs['usrid']

        # expecting where
        where = data['where']
        patch = data['patch']

        # validate patch
        # init modelClass for this doc
        patch_errors = validate(modelClass, patch)
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
        resp = db.command('findAndModify', collNam,
            query = where,
            update = {"$set": patch},
            new = True
        )

        # only return if error condition exists
        response['collection'] = collNam
        response['total_invalid'] = 0
        response['id'] = id.__str__()

        # remove this, not needed
        response['doc'] = resp['value']

        return {'response': response, 'status_code': status}

    def get(self, **kwargs):
        """Docstring for get method:"""
        db = self.db
        class_name = kwargs['class_name']
        modelClass = getattr(models, class_name)
        collNam = modelClass.meta['collection']
        coll = db[collNam]

        response = {}
        docs = []
        status = 200

        # if an id was passed, try to return only that one
        if 'id' in kwargs:
            id = kwargs['id']
            doc = coll.find_one({"_id": ObjectId(id)})
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
            cursor = coll.find(spec = where, fields = fields, skip = skip, limit = limit).sort(sorts)
        else:
            cursor = coll.find(spec = where, fields = fields, skip = skip, limit = limit)
        for doc in cursor:
            docs.append(doc)

        # handle any virtual fields
        if 'vflds' in kwargs:
            vflds = kwargs['vflds']
            for i, doc in enumerate(docs):
                initialed_model = modelClass(**doc)
                for vfld in vflds:
                    docs[i][vfld] = getattr(initialed_model, vfld)

        response['docs'] = docs

        return {'response': response, 'status_code': status}

