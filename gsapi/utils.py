import re
import os
import json

from bson.json_util import dumps, loads
import bson.json_util as bson_json_util
from extensions import validate

from flask import redirect
from werkzeug.routing import HTTPException, RoutingException

#from models import model_classes_by_id
import models

def load_data(db, json_filepath):
    '''Bulk load from json into corresponding collections.
    Each item is expected to contain '_cls' which represents the model class and the collection it belongs to.
    Validation rules are tested for each doc.
    '''

    # let's grab the data, error check?
    data  = open(json_filepath).read()

    data  = bson_json_util.loads(data)

    response     = {}
    status       = 200
    docs         = []

    load_errors  = []
    total_errors = 0
    total_added  = 0

    for doc in data:
        class_id        = doc['_c']
        model           = getattr(models, class_id)
        collection_name = model.meta['collection']
        collection      = db[collection_name]
        errors          = {}

        # Validate
        doc_errors    = validate(model, doc)
        if doc_errors:
            total_errors += doc_errors['count']
            load_errors.append(doc_errors)
            continue

        # init model for this doc
        initialized_model    = model(**doc)
        
        #log date time user involved with this event
        # m.logit(user_id, 'post')
        
        # need to stuff into mongo
        doc_validated        = initialized_model.to_python()
        
        dumped               = bson_json_util.dumps(doc_validated)
        doc_info             = {}
        doc_validated['_id'] = doc['_id']
        doc_validated['_id'] = collection.save(doc_validated, safe=True)
        docs.append(doc_validated)
        total_added += 1

    response['total_inserted'] = len(docs)

    if load_errors:
        response['total_invalid'] = len(load_errors)
        response['errors']        = load_errors
        response['total_errors']  = total_errors
        status                    = 400
    else:
        response['total_invalid'] = 0


    response['docs'] = docs

    print "{count} docs loaded from: {json_filepath}!".format(count=total_added, json_filepath=json_filepath)

    return {'response':response, 'status':status}



def slugify(value):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Copy/Pasted from ametaireau/pelican/utils itself took from django sources.
    """
    if type(value) == unicode:
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


class Redirect303(HTTPException, RoutingException):
    """Raise if the map requests a redirect. This is for example the case if
    `strict_slashes` are activated and an url that requires a trailing slash.

    The attribute `new_url` contains the absolute destination url.
    """
    code = 303

    def __init__(self, new_url):
        RoutingException.__init__(self, new_url)
        self.new_url = new_url

    def get_response(self, environ):
        return redirect(self.new_url, 303)

