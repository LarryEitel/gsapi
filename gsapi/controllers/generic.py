# -*- coding: utf-8 -*-
import os
import json
from extensions import validate
from jsondatetime import loads
import json
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import re
import datetime
import models

def get(db, **kwargs):
    class_name = kwargs['class_name']
    model           = getattr(models, class_name)
    collection_name = model.meta['collection']
    collection      = db[collection_name]

    response = {}
    docs     = []
    status   = 200

    # if an id was passed, try to return only that one
    if 'id' in kwargs:
        id = kwargs['id']
        doc = collection.find_one({"_id": ObjectId(id)})
        docs.append(doc)
        response['docs'] = docs
        return {'response': response, 'status': status}



    if 'where' in kwargs:
        where = json.loads(kwargs['where'], object_hook=json_util.object_hook)
    else:
        where = {}

    # this allows us to filter results on the type of contact involved
    # contacts return all
    # persons return contacts that are persons, etc.
    where['_c']           = class_name

    fields                  = json.loads(kwargs['fields']) if 'fields' in kwargs else None
    sort_raw                  = json.loads(kwargs['sort']) if 'sort' in kwargs else None

    # mongo wants sorts like: [("fld1", <order>), ("fld2", <order>)]
    sorts                   = []
    if sort_raw:
        flds = sort_raw
        for fld in flds:
            sorts = [(k,int(v)) for k,v in fld.iteritems()]

    skip       = int(json.loads(kwargs['skip'])) if 'skip' in kwargs else 0
    limit       = int(json.loads(kwargs['limit'])) if 'limit' in kwargs else 0
    skip_limit = skip > -1 and limit

    if sorts:
        cursor = collection.find(spec=where, fields=fields, skip=skip, limit=limit).sort(sorts)
    else:
        cursor = collection.find(spec=where, fields=fields, skip=skip, limit=limit)
    for doc in cursor:
        docs.append(doc)

    # handle any virtual fields
    if 'vflds' in kwargs:
        vflds = json.loads(kwargs['vflds'])
        #vflds = kwargs['vflds']
        for i, doc in enumerate(docs):
            initialed_model = model(**doc)
            for vfld in vflds:
                docs[i][vfld] = getattr(initialed_model, vfld)


    response['docs'] = docs

    return {'response': response, 'status': status}

















    print class_name