# -*- coding: utf-8 -*-
import os
import re
import datetime
from bson import ObjectId
import models
import globals
from schematics.serialize import (to_python, to_json, make_safe_python,
                                  make_safe_json, blacklist, whitelist)
from models.extensions import validate, validate_partial, doc_remove_empty_keys, nextEId
from models.logit import logit
from models.typ import Typ
from models._cs import _cs
from utils.nextid import nextId
from utils.slugify import slugify

def preSave(doc, usr):
    response   = {}
    
    modelClass = getattr(models, doc['_c'])
    # collNam    = modelClass.meta['collection']
    # collNamTmp = collNam + '_tmp'
    # collTmp    = db[collNamTmp]
    # coll       = db[collNam]

    # validate
    errors     = validate_partial(modelClass, doc)

    if errors:
        response['errors'] = errors['errors']
        response['total_errors'] = errors['count']
        return {'response': response, 'status': 400}
    
    # init model instance
    model      = modelClass(**doc)
    
    # if there is a vNam class property 
    if hasattr(model, 'vNam') and 'dNam' in model._fields:
        model.dNam = model.vNam
        if hasattr(model, 'vNamS') and 'dNamS' in model._fields:
            model.dNamS = model.vNamS
            
        doc        = doc_remove_empty_keys(to_python(model, allow_none=True))
    
    # logit update
    doc = logit(usr, doc)
    response['doc'] = doc
    return {'response': response, 'status': 200}
def initDocListTypes(doc, usr):
    '''When posting a doc with listType attributes/fields, they must be initialized with provided data and validated and saved back to the doc for further handling, ie, validation, etc.'''
    attrNams = doc.keys()
    # loop through all doc keys
    for attrNam in attrNams:
        attrVal = doc[attrNam]

        # is it a list
        if type(attrVal) == list:
            attrValList = attrVal 

            # loop through all the elements in the list
            for attrValListOffset in range(0, len(attrValList)):
                attrValListItem = attrValList[attrValListOffset]
                attr_c          = attrValListItem['_c']
                modelClass      = _cs[attr_c]['modelClass']

                # init a class model for this item
                model           = modelClass()

                # set model attribute values
                for k,v in attrValListItem.iteritems(): setattr(model, k, v)

                # generate a next eId
                resp       = nextEId(doc, attrNam)
                doc        = resp['doc']
                model.eId  = resp['eId']   
                
                # generate dNam
                if hasattr(model, 'vNam') and 'dNam' in model._fields and not model.dNam:
                    model.dNam = model.vNam 

                # generate dNamS
                if 'dNamS' in model._fields and hasattr(model, 'vNamS') and not model.dNamS:
                    model.dNamS = model.vNamS

                # remove all empty fields
                attrValListItemClean   = doc_remove_empty_keys(to_python(model, allow_none=True))

                # validate
                errors = validate(modelClass, attrValListItemClean)

                # TODO: handle and test errors
                if errors:
                    total_errors += errors['count']
                    post_errors.append(errors)
                    continue                    
                
                # logit update
                attrValListItemClean = logit(usr, attrValListItemClean, method='post')                   
                # save cleaned listType item back to doc
                doc[attrNam][attrValListOffset] = attrValListItemClean
                
    # now all listType items are clean, validated, and logged
    return doc
              
class Generic(object):

    def __init__(self, g):
        #: Doc comment for instance attribute db
        self.usr = g['usr']
        self.db  = g['db']
        self.es  = g['es']
        
    def post_attr(self, doc, attrNam, attr_c, attrVal, useTmpDoc = True):
        ''' 
            doc     = base doc to post/add attrVal to (in the attrNam field) 
                Must contain _c, and _id
            usr     = user object
            coll    = collection
            attr_c  = model class
            _id     = doc id
            attrNam = attribute/fieldname
            attrVal = value to post/add
            '''

        db           = self.db
        
        errors       = {}
        doc_info     = {}
        response     = {}
        status       = 200
        post_errors  = []
        total_errors = 0
        
        
        doc_id         = doc['_id']        
        usrOID       = self.usr['OID']
        where        = {'_id': doc_id}
        doc_c          = doc['_c']
        docModel       = _cs[doc_c]['modelClass']()
        collNam      = docModel.meta['collection']
        coll         = db[collNam + '_tmp'] if useTmpDoc else db[collNam]
        
        attrModel    = _cs[attr_c]['modelClass']()
        
        

        for k,v in attrVal.iteritems(): setattr(attrModel, k, v)
        
        # set the next element id eId
        resp       = nextEId(doc, attrNam)

        doc        = resp['doc']
        
        attrModel.eId  = resp['eId']
        
        if hasattr(attrModel, 'vNam') and 'dNam' in attrModel._fields and not attrModel.dNam:
            attrModel.dNam = attrModel.vNam

        # set dNamS if used:
        # if dNamS is empty, set to value of slug
        if hasattr(attrModel, 'vNam') and 'dNamS' in attrModel._fields and not attrModel.dNamS:
            attrModel.dNamS = attrModel.vNamS

        attrValClean   = doc_remove_empty_keys(to_python(attrModel, allow_none=True))
        attrErrors = validate(_cs[attr_c]['modelClass'], attrValClean)
        if attrErrors:
            response['total_invalid'] = 1
            response['errors']        = attrErrors
            response['total_errors']  = 1
            return {'response': response, 'status': 400} 
        
        # logit update
        attrValClean = logit(self.usr, attrValClean, method='post')
        
        resp = coll.update(where,
                {"$push": { attrNam: attrValClean}, "$set": {'eIds': doc['eIds']}}
            )
        
        response['update_response'] = resp

        return {'response': response, 'status': 200} 



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
        
        usrOID       = self.usr['OID']
        docs_to_post = kwargs['docs']
        
        post_errors  = []
        total_errors = 0

        for doc in docs_to_post:
            errors      = {}
            doc_info    = {}

            # required attribute
            _c          = doc['_c']

            # shortcut
            doc_keys   = doc.keys()     
            
            modelClass = getattr(models, _c)
            _id        = doc['_id'] if '_id' in doc_keys else None
            where      = {'_id': ObjectId(_id)} if _id else None
            attrNam    = doc['attrNam'] if 'attrNam' in doc_keys else None
            attr_c     = doc['attr_c'] if attrNam else None
            attrVal    = doc['attrVal'] if attrNam else None
            collNam    = modelClass.meta['collection']
            collTmp    = db[collNam + '_tmp']
            coll       = db[collNam]

            # if _ id is passed,  it directs that a temp doc be initialized and inserted into the appropriate Tmp (temp) collection.
            # if an _id IS passed, it directs that the doc passed in be validated and inserted in the base collection and the temp doc in the temp collection be deleted.
            
            # if attrNam, posting a new value to a listtype attribute/field
            if attrNam:
                for elem in attrVal:
                    modelClass = getattr(models.embed, attr_c)
                    model      = modelClass()
                    for k,v in elem.iteritems(): setattr(model, k, v)
                    
                    resp       = nextEId(doc, attrNam)
                    doc        = resp['doc']
                    # model.eIds = doc['eIds']
                    model.eId  = resp['eId']
                    
                    if hasattr(model, 'vNam') and 'dNam' in model._fields and not model.dNam:
                        model.dNam = model.vNam

                    # generate a slug if slug is empty
                    if 'slug' in model._fields and 'dNam' in model._fields and not model.slug:
                        model.slug = slugify(model.dNam, coll)

                    # set dNamS if used:
                    # if dNamS is empty, set to value of slug
                    if 'dNamS' in model._fields and not model.dNamS:
                        if hasattr(model, 'vNamS'):
                            model.dNamS = model.vNamS
                        else:
                            model.dNamS = model.slug


                    embedDoc   = doc_remove_empty_keys(to_python(model, allow_none=True))
                    doc_errors = validate(modelClass, embedDoc)
                    
                    if doc_errors:
                        total_errors += doc_errors['count']
                        post_errors.append(doc_errors)
                        continue                    
                    
                    embedDoc['_c'] = attr_c
                    
                    # logit update
                    embedDoc = logit(self.usr, embedDoc, method='post')
                    
                    collTmp.update(where,
                            {"$push": { attrNam: embedDoc}, "$set": {'eIds': doc['eIds']}}
                        )
                    

                    doc_info['doc']   = embedDoc
                    docs.append(doc_info)   
                               
                # http://docs.mongodb.org/manual/applications/update/
                # { $set: { 'emails.$.eId': 2 }
        
                response['total_inserted'] = len(docs)
        
                if post_errors:
                    response['total_invalid'] = len(post_errors)
                    response['errors']        = post_errors
                    response['total_errors']  = total_errors
                    status                    = 400
                else:
                    response['total_invalid'] = 0
        
                response['docs'] = docs
        
                return {'response': response, 'status': status}                
                
            # Initialize a temp (tmp) doc if no OID and no data.
            elif not '_id' in doc_keys and len(doc_keys) == 1:
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
                tmp_doc = logit(self.usr, tmp_doc)
                
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
            
            # need to cruz through all doc keys to handle arrays/listtype fields.
            # they need to be initialized according to the appropriate model and validated, etc.
            doc = initDocListTypes(doc, self.usr)

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
                response = nextId(coll)
                if response['status'] == 200:
                    model.dId = response['nextId']
                else:
                    # handle error condition
                    pass

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
                doc = logit(self.usr, doc, 'post')

            doc['_c'] = _c
            doc_clean = doc_remove_empty_keys(doc)
            
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

        return {'response': response, 'status': status}
    
    def put(self, **kwargs):
        """Update a doc"""
        db = self.db
        # TODO: accomodate where clause to put changes to more than one doc.
        
        usrOID     = self.usr['OID']
        data       = kwargs['data']
        _c         = data['_c']
        modelClass = getattr(models, _c)
        #attrNam    = doc['attrNam'] if 'attrNam' in doc_keys else None
        #attr_c     = doc['attr_c'] if attrNam else None
        #attrEid    = doc['attrEid'] if attrNam else None
        #attrVal    = doc['attrVal'] if attrNam else None
        collNam    = modelClass.meta['collection']
        collNamTmp = collNam + '_tmp'
        collTmp    = db[collNamTmp]
        coll       = db[collNam]
        
        response   = {}
        docs       = []
        status     = 200
        
        where      = data['where']
        patch      = data['patch']
        eId        = data['eId'] if 'eId' in data else None
        
        if eId and len(patch.keys()) > 1:
            # TODO Handle error
            pass

        # if element eId was passed, expect to put/patch change to one element in a ListType attribute/field
        if eId and len(patch) == 1:
            elem    = patch.popitem()
            attrNam = elem[0]

            # enhance to support putting/updating multiple list elements
            attrVal = elem[1][0]
            
            resp    = preSave(attrVal, self.usr)
            if not resp['status'] == 200:
                return {'response': resp, 'status': 400}
            
            attrVal = resp['response']['doc']
            # http://docs.mongodb.org/manual/applications/update/
            # patch update in tmp collection
            attrEl = attrNam + '.$'
            doc = collTmp.find_and_modify(
                query = where,
                update = { "$set": { attrEl: attrVal }},
                new = True
            )
            response['collection'] = collNamTmp
            response['total_invalid'] = 0
            response['id'] = id.__str__()
    
            # remove this, not needed
            response['doc'] = doc

            return {'response': response, 'status': 200}
        else:
            # validate patch
            # init modelClass for this doc
            patch_errors = validate_partial(modelClass, patch)
            if patch_errors:
                response['errors'] = patch_errors['errors']
                response['total_errors'] = patch_errors['count']
                status = 400
    
                return prep_response(response, status = status)
    
            # logit update
            patch = logit(self.usr, patch)
                    
            # patch update in tmp collection
            doc = collTmp.find_and_modify(
                query = where,
                update = {"$set": patch},
                new = True
            )

        # init model instance
        model      = modelClass(**doc)
        
        # if there is a vNam class property 
        if hasattr(model, 'vNam') and 'dNam' in model._fields:
            doc        = collTmp.find_one(where)
            _id        = doc['_id']
            
            model.dNam = model.vNam
            if hasattr(model, 'vNamS') and 'dNamS' in model._fields:
                model.dNamS = model.vNamS
                
            doc        = doc_remove_empty_keys(to_python(model, allow_none=True))
            collTmp.update(where, doc)
            # gotta put the _id back
            doc['_id'] = _id


        response['collection'] = collNamTmp
        response['total_invalid'] = 0
        response['id'] = id.__str__()

        # remove this, not needed
        response['doc'] = doc

        return {'response': response, 'status': status}

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
            return {'response': response, 'status': status}



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

        return {'response': response, 'status': status}

