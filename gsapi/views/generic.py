# -*- coding: utf-8 -*-
from flask import make_response, jsonify, abort
import os
import json
from extensions import validate
from jsondatetime import loads
import mimerender
import json
from flask import request
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import re
import datetime
from flask import current_app
import models
import controllers

mimerender  = mimerender.FlaskMimeRender()

render_xml  = lambda message: '<message>%s</message>'%message
render_json = lambda **args: dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt  = lambda message: message

def get_document_link(model_name, id):
    return "http://localhost:5000/%s/%s" % (model_name, id)


def json_renderer(**data):
    return jsonify(loads(dumps(data)))

def prep_response(dct, status=200):
    #mime, render = get_best_mime()
    renderer = json_renderer
    mime = 'Content-Type: application/json'
    #rendered = globals()[render](**dct)
    rendered = renderer(**dct)
    resp = make_response(rendered, status)
    resp.mimetype = mime
    return resp


def post(class_name):
    from db import db

    docs_to_post = json.loads(request.data, object_hook=json_util.object_hook)

    # if a dict, then stuff it into a list
    if type(docs_to_post) == dict: docs_to_post = [docs_to_post]

    args = dict(request.view_args.items() + request.args.items())
    args['docs'] = docs_to_post

    response = controllers.generic.post(db, **args)

    return prep_response(response['response'], status = response['status_code'])


def put(class_name):
    from db import db

    data          = json.loads(request.data, object_hook=json_util.object_hook)
    
    args          = dict(request.view_args.items() + request.args.items())
    args['data']  = data
    args['usrid'] = "50468de92558713d84b03fd7"
    
    response      = controllers.generic.put(db, **args)

    return prep_response(response['response'], status = response['status_code'])



# def put(class_name):
#     from db import db

#     model           = getattr(models, class_name)
#     collection_name = model.meta['collection']

#     user_id = "50468de92558713d84b03fd7"

#     response = {}
#     status   = 200
#     docs     = []

#     # let's deserialize mongo objects
#     data = json.loads(request.data, object_hook=json_util.object_hook)

#     # expecting where
#     where = data['where']
#     patch = data['patch']

#     # validata patch
#     # init model for this doc
#     patch_errors    = validate(model, patch)
#     if patch_errors:
#         response['errors']        = patch_errors['errors']
#         response['total_errors']  = patch_errors['count']
#         status                    = 400

#         return prep_response(response, status = status)

#     # until we get signals working
#     # manually include modified event details
#     # patch['mBy'] = user_id
#     patch['mBy'] = ObjectId(user_id)
#     patch['mOn'] = datetime.datetime.utcnow()

#     # https://github.com/mongodb/mongo-python-driver/blob/master/pymongo/collection.py#L1035
#     resp = db.command('findAndModify', collection_name,
#         query = where,
#         update = {"$set": patch},
#         new = True
#     )

#     response['collection']    = collection_name
#     response['total_invalid'] = 0
#     response['id']            = id.__str__()
#     response['doc']           = resp['value']

#     return prep_response(response, status = status)


def patch_embedded(collection, id, embedded):
    # get collection name for this model
    col  = models[collection].meta['collection']
    _cls = models[collection].meta['_c']


    user_objectId = ObjectId("50468de92558713d84b03fd7")

    response = {}
    status   = 200
    docs     = []


    # grab data and parse
    js = json.loads(request.data)

    # what is the doc class for these docs to embed
    field_name = js['field_name']
    _cls       = js['_c']


    # Retrieve base doc to insert new embedded docs
    doc_to_patch   = mongo.db[col].find_one({"_id":ObjectId(id)})
    if not doc_to_patch:
        return 'error'
    base_model = models[col](**doc_to_patch)
    #log date time user involved with this event
    base_model.logit(user_objectId, 'patch')

    # docs to insert
    original_values    = js['original_values']
    key_field          = original_values['key_field']

    replacement_values = js['replacement_values']

    # need to get the position of original embedded doc to update
    embedded_pos = [i for i,x in enumerate([x[key_field] for x in doc_to_patch[field_name]]) if x == original_values['value']]
    if not embedded_pos:
        return 'error: did not find item to replace'

    embedded_pos = embedded_pos[0]
    elem = doc_to_patch[field_name][embedded_pos]
    print 'found', elem
    for fld, val in replacement_values.iteritems():
        print fld, val
        elem[fld] = val
    print 'replacement_values', replacement_values
    print 'updated', elem
    # replace this element with new one
    doc_to_patch[field_name][embedded_pos] = elem

    doc = mongo.db[col].update({"_id":ObjectId(id)}, {"$set": {"%s" % field_name:doc_to_patch[field_name]}})

    post_errors        = []
    total_errors       = 0

    # make sure doc_to_path exists

    # Validate
    doc_errors = validate(models[field_name], replacement_values)

    if doc_errors:
        total_errors += doc_errors['count']
        post_errors.append(doc_errors)
    else:
        doc_model   = models[field_name](**doc)

        doc_info         = {}
        doc_info['doc']  = doc_model.to_python()

        docs.append(doc_model)


    response['total_inserted'] = len(docs)
    if post_errors:
        response['total_invalid'] = len(post_errors)
        response['errors']        = post_errors
        response['total_errors']  = total_errors
        status                    = 400
    else:
        response['total_invalid'] = 0

        for doc in docs:
            base_model.emails.insert(1, doc)

        js  = base_model.to_python()
        doc = mongo.db[col].update({"_id":ObjectId(id)}, {"$set": js})

    response[collection] = docs

    return prep_response(response, status = status)
def post_embedded(collection, id, embedded):
    # get collection name for this model
    col  = models[collection].meta['collection']
    _cls = models[collection].meta['_c']

    user_objectId = ObjectId("50468de92558713d84b03fd7")

    response = {}
    status   = 200
    docs     = []

    # Retrieve base doc to insert new embedded docs
    base_doc   = mongo.db[col].find_one({"_id":ObjectId(id)})
    base_model = models[col](**base_doc)

    #log date time user involved with this event
    base_model.logit(user_objectId, 'patch')

    # grab data and parse
    js = json.loads(request.data)

    # what is the doc class for these docs to embed
    field_name = js['field_name']
    _cls       = js['_c']

    # docs to insert
    docs_to_post       = js['docs']

    # if a dict, then stuff it into a list
    if type(docs_to_post) == dict: docs_to_post = [docs_to_post]

    post_errors = []
    total_errors = 0
    for doc in docs_to_post:
        # Validate
        doc_errors = validate(models[field_name], doc)

        if doc_errors:
            total_errors += doc_errors['count']
            post_errors.append(doc_errors)
            continue

        doc_model   = models[field_name](**doc)

        doc_info         = {}
        doc_info['doc']  = doc_model.to_python()

        docs.append(doc_model)


    response['total_inserted'] = len(docs)
    if post_errors:
        response['total_invalid'] = len(post_errors)
        response['errors']        = post_errors
        response['total_errors']  = total_errors
        status                    = 400
    else:
        response['total_invalid'] = 0

        for doc in docs:
            base_model.emails.insert(1, doc)

        js  = base_model.to_python()
        doc = mongo.db[col].update({"_id":ObjectId(id)}, {"$set": js})

    response[collection] = docs

    return prep_response(response, status = status)

# def post(class_name):
#     from db import db

#     model           = getattr(models, class_name)
#     collection_name = model.meta['collection']

#     collection      = db[collection_name]
#     response        = {}
#     status          = 200
#     docs            = []

#     # let's deserialize mongo objects
#     docs_to_post = json.loads(request.data, object_hook=json_util.object_hook)

#     # if a dict, then stuff it into a list
#     if type(docs_to_post) == dict: docs_to_post = [docs_to_post]

#     post_errors = []
#     total_errors = 0
#     for doc in docs_to_post:
#         errors = {}
#         user_id = "50468de92558713d84b03fd7"

#         # need to stuff in class_name
#         doc['_c']     = class_name

#         # Validate
#         doc_errors    = validate(model, doc)
#         if doc_errors:
#             total_errors += doc_errors['count']
#             post_errors.append(doc_errors)
#             continue

#         # init model for this doc
#         m   = model(**doc)

#         #log date time user involved with this event
#         m.logit(user_id, 'post')

#         # need to stuff into mongo
#         doc_validated    = m.to_python()
#         try:
#             doc_validated['_c'] = m.meta['_c']
#         except:
#             pass

#         dumped = dumps(doc_validated)
#         doc_info         = {}

#         id               = str(collection.insert(doc_validated, safe=True))
#         doc_info['id']   = id
#         doc_info['doc']  = doc_validated
#         doc_info['link'] = get_document_link(class_name, id)

#         docs.append(doc_info)

#     response['total_inserted'] = len(docs)

#     if post_errors:
#         response['total_invalid'] = len(post_errors)
#         response['errors']        = post_errors
#         response['total_errors']  = total_errors
#         status                    = 400
#     else:
#         response['total_invalid'] = 0

#     response['docs'] = docs

#     return prep_response(response, status = status)




def get(class_name, id=None):
    from db import db

    args = dict(request.view_args.items() + request.args.items())

    resp = controllers.generic.get(db, **args)

    return prep_response(resp['response'], status = resp['status_code'])

def remove(collection, id):
    col = models[model].meta['collection']
    return db[col].remove({"_id":ObjectId(id)})
