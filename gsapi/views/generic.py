# -*- coding: utf-8 -*-
from flask import make_response, jsonify, abort
import os
import json
import mimerender
import json
from flask import request
from bson import ObjectId
from bson.json_util import dumps
from bson import json_util
import re
import datetime
from flask import current_app

from gsapi import models, controllers
from gsapi.utils import mongo_json_object_hook
from gsapi.extensions import validate
from gsapi.jsondatetime import loads

mimerender  = mimerender.FlaskMimeRender()

render_xml  = lambda message: '<message>%s</message>'%message
render_json = lambda **args: dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt  = lambda message: message

def get_document_link(model_name, id):
    '''
    Returns the link to the document
    
    Parameters:
        model_name - 
        id - 
        
    Returns
        The document link
    '''
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

def home(models):
    response = {}
    links    = []
    host     = request.url
    for model in models:
        links.append("<link rel='child' title='---%(name)s' href='%(modelURI)s' />" %
            {'name':model, 'modelURI': host + model})
    response['links'] = links
    return prep_response(response, status = 200)

def post(class_name):
    from db import db
    generic  = controllers.Generic(db)

    #data = loads(request.data)
    data = request.data

    docs_to_post = json.loads(data, object_hook=json_util.object_hook)

    # if a dict, then stuff it into a list
    if type(docs_to_post) == dict: docs_to_post = [docs_to_post]

    args = dict(request.view_args.items() + request.args.items())
    args['docs'] = docs_to_post

    response = generic.post(**args)

    return prep_response(response['response'], status = response['status_code'])


def put(class_name):
    from db import db
    generic  = controllers.Generic(db)

    data          = json.loads(request.data, object_hook=json_util.object_hook)

    args          = dict(request.view_args.items() + request.args.items())
    args['data']  = data
    args['usrid'] = "50468de92558713d84b03fd7"

    response      = generic.put(**args)

    return prep_response(response['response'], status = response['status_code'])

def get(class_name, id=None):
    from db import db
    generic  = controllers.Generic(db)

    parsed_args = {}
    for k, v in dict(request.args.items()).iteritems():
        parsed_args[k] = json.loads(v, object_hook=mongo_json_object_hook)


    args = dict(request.view_args.items() + parsed_args.items())
    #args = dict(request.view_args.items() + request.args.items())


    #if 'where' in args:
        #args['where'] = dumps(json.loads(args['where'], object_hook=mongo_json_object_hook))

    resp = generic.get(**args)

    links    = []
    host     = 'http://' + request.environ['HTTP_HOST']
    links.append("<link rel='parent' title='%(name)s' href='%(modelURI)s' />" %
            {'name':class_name, 'modelURI': host + class_name})
    links.append("<link rel='model' title='%(name)s' href='%(modelURI)s' />" %
            {'name':class_name, 'modelURI': host + class_name})

    # need to add a link to each doc along with etag and updated i
    # links.append("<link rel='model' title='%(name)s' href='%(modelURI)s' />" %
    #         {'name':class_name, 'modelURI': host + class_name})

    resp['response']['links'] = links

    return prep_response(resp['response'], status = resp['status_code'])




def remove(collection, id):
    col = models[model].meta['collection']
    return db[col].remove({"_id":ObjectId(id)})

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
