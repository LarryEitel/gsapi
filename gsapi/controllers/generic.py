# -*- coding: utf-8 -*-
import os
import re
import datetime
from bson import ObjectId
import models
from schematics.serialize import (to_python, to_json, make_safe_python,
                                  make_safe_json, blacklist, whitelist)
from models.extensions import validate, validate_partial
from models.logit import logit
from utils.nextid import nextId
from utils.slugify import slugify

class Generic(object):

    def __init__(self, db, es = None):
        #: Doc comment for instance attribute db
        self.db = db
        self.es = es
    
    def post(self, **kwargs):
        '''Insert a doc
            newDocTmp: Initialize a temp (tmp) doc if no OID and no data.
            cloneDocTmp: Clone to a temp doc if OID and no isTmp flag set.
            upsertDocTmp: Update or Insert temp doc to base collection if OID and isTmp is set.
            insertDoc: Insert a new doc if no OID and there are more attributes than _c.
            '''
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
            doc_info   = {}
                   
            # required attribute
            _c         = doc['_c']
            
            # shortcut
            doc_keys    = doc.keys()     
            
            modelClass = getattr(models, _c)
            _id        = doc['_id'] if '_id' in doc_keys else None
            collNam    = modelClass.meta['collection']
            collTmp    = db[collNam + '_tmp']
            coll       = db[collNam]
            

            # if _ id is passed,  it directs that a temp doc be initialized and inserted into the appropriate Tmp (temp) collection.
            # if an _id IS passed, it directs that the doc passed in be validated and inserted in the base collection and the temp doc in the temp collection be deleted.
            
            # Initialize a temp (tmp) doc if no OID and no data.
            if not '_id' in doc_keys and len(doc_keys) == 1:
                newDocTmp = True
                useTmpDoc = True
                
            # Clone to a temp doc if OID and no isTmp flag set.
            elif '_id' in doc_keys and not 'isTmp' in doc_keys and len(doc_keys) > 2:
                cloneDocTmp  = True
                useTmpDoc    = True
                
                
                # find source doc
                # set locked = True                
                doc_cloned = coll.find_and_modify(
                    query = {'_id':_id},
                    update = {"$set": {'locked': True}},
                    new = True
                )                
                # set cloned doc in tmp collection isTmp = True  
                doc_cloned['isTmp'] = True
                
                # don't need locked set in tmp doc 
                del doc_cloned['locked']
                
                # clone/save doc to tmp collection

                # TODO properly handle exception
                try:
                    collTmp.insert(doc_cloned)
                except:
                    pass                  
                        
                doc_info['doc']   = doc_cloned
                
                # TODO
                # should return a link to object according to good practice
                #doc_info['link'] = get_document_link(class_name, id)
    
                docs.append(doc_info)   
                
                continue
                
            # Update temp doc to base collection if OID and isTmp is set.
            elif '_id' in doc_keys and 'isTmp' in doc_keys and doc['isTmp']:
                upsertDocTmp  = True
                useTmpDoc     = False

                tmp_doc = collTmp.find_one({'_id': _id})
                
                # unset isTmp
                _id = tmp_doc['_id']
                tmp_doc['locked'] = False
                del tmp_doc['_id']             
                del tmp_doc['isTmp']             
                
                # logit update
                tmp_doc = logit(usrOID, tmp_doc)
                
                # update original/source doc
                doc = coll.update({'_id': _id}, {"$set": tmp_doc}, upsert=True, safe=True)
                
                # remove tmp doc
                collTmp.remove({'_id': _id})
                
                # though not necessary, to be consistant, return full doc
                doc = coll.find_one({'_id': _id})
                
                doc_info['doc']   = doc  
                docs.append(doc_info)  
                
                continue
                
            # Insert a new doc if no OID and there are more attributes than _c.
            elif not '_id' in doc_keys and len(doc_keys) > 2:
                insertDoc  = True
                useTmpDoc  = False
            
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
            doc             = to_python(model, allow_none=True)

            # do not log if using temp doc
            #log date time user involved with this event
            if not useTmpDoc:
                doc = logit(usrOID, doc, 'post')

            doc_clean       = {}
            doc_clean['_c'] = _c
            for k, v in doc.iteritems():
                if doc[k]:
                    doc_clean[k] = doc[k]
            
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
        """Update a doc"""
        db = self.db
        # TODO: accomodate where clause to put changes to more than one doc.
        
        usrOID     = kwargs['usrOID']
        data       = kwargs['data']
        _c         = data['_c']
        modelClass = getattr(models, _c)
        collNam    = modelClass.meta['collection']
        collNamTmp = collNam + '_tmp'
        collTmp    = db[collNamTmp]
        coll       = db[collNam]
        
        response   = {}
        docs       = []
        status     = 200
        
        
        # expecting where
        where      = data['where']
        patch      = data['patch']

        # validate patch
        # init modelClass for this doc
        patch_errors = validate_partial(modelClass, patch)
        if patch_errors:
            response['errors'] = patch_errors['errors']
            response['total_errors'] = patch_errors['count']
            status = 400

            return prep_response(response, status = status)

        # logit update
        patch = logit(usrOID, patch)
                
        # patch update in tmp collection
        doc = collTmp.find_and_modify(
            query = where,
            update = {"$set": patch},
            new = True
        )

        # need to handle case where model has a dNam, etc. which may have been affected by patch

        # init model instance
        model      = modelClass(**doc)
        
        # if there is a vNam class property 
        if hasattr(model, 'vNam') and 'dNam' in model._fields:
            doc        = collTmp.find_one(where)
            _id        = doc['_id']
            model.dNam = model.vNam
            if hasattr(model, 'vNamS') and 'dNamS' in model._fields:
                model.dNamS = model.vNamS
                
            doc        = to_python(model, allow_none=True)
            doc_clean  = {'_c': _c}
            for k, v in doc.iteritems():
                if doc[k]:
                    doc_clean[k] = doc[k]
            doc = doc_clean
            collTmp.update(where, doc)
            # gotta put the _id back
            doc['_id'] = _id


        response['collection'] = collNamTmp
        response['total_invalid'] = 0
        response['id'] = id.__str__()

        # remove this, not needed
        response['doc'] = doc

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

