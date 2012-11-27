import re
import os
import json
import jsondatetime # https://github.com/nicolaiarocci/json-datetime
from bson.json_util import dumps, loads
import bson.json_util as bson_json_util
from bson import ObjectId
from models.extensions import validate
import datetime
from flask import redirect
from werkzeug.routing import HTTPException, RoutingException

#from models import model_classes_by_id
import models
import dateutil.parser

reobj_oid = re.compile(r'\{\s*"\$oid"\s*:\s*"(.*?)"\s*\}')
reobj_objectid = re.compile(r'ObjectId\("(.*?)"\)', re.IGNORECASE)
reobj_date = re.compile(r'\{\s*"\$date"\s*:\s*(\d+)\s*\}')
reobj_date_with_dot = re.compile(r'\{\s*"\$date"\s*:\s*(\d+)\.(\d+)\s*\}')
reobj_isodate = re.compile(r'ISODate\("(.*?)"\)', re.IGNORECASE)

def preparse_json_doc(jstr):
    ''' Preparse to better identify ObjectId's and DateTimes
    Preparse json file which may have been come from mongoexport or MongoVue dump or hand edited.

    OBJECTIDs

    # as exported by mongoexport
    Convert:    { "$oid" : "50536c4c2558712e205a269a" }
    To:         "$oid:50536c4c2558712e205a269a"

    # as exported by MongoVue
    Convert:    ObjectId("50536c4c2558792f205a299d")
    To:         "$oid:50536c4c2558792f205a299d"

    DATES

    # as exported by mongoexport
    Convert:    { "$date" : 1347644492471 }
    To:         "$date:1347644492471"

    # If someone wants to manually set a datetime in more human readable form. Good for testing.
    Convert:    ISODate("2012-09-14T17:41:32.471Z")
    To:         "$isodate:2012-09-14T17:41:32.471Z"

    One motivation was that the json.loads object_hook could not handle values that dictionaries. For example:
            "oBy" : { "$oid" : "50468de92558713d84b03fd7" }

            object_hook function would hook dict.key "$oid" along with numeric value. This needs to be converted to an ObjectId("50468de92558713d84b03fd7") as a value of "oBy".
            Ultimately the ultimate result should be:
                "oBy" : ObjectId("50468de92558713d84b03fd7")

                This is what will be sent to MongoDb!
    '''
    jstr = reobj_oid.sub(r'"$oid:\1"', jstr)
    jstr = reobj_objectid.sub(r'"$oid:\1"', jstr)
    jstr = reobj_date.sub(r'"$date:\1"', jstr)
    jstr = reobj_date_with_dot.sub(r'"$date:\1\2"', jstr)
    jstr = re.sub(r'"\s*\$date"\s*:\s*(\d+)\.(\d+)', r'"$date:\1\2"', jstr)
    jstr = reobj_isodate.sub(r'"$isodate:\1"', jstr)
    return jstr

def mongo_json_object_hook(dct):
    for k, v in dct.items():
        if v[0:4] == '$oid':
            dct[k] = ObjectId(v[5:])
        elif v[0:5] == '$date':
            dct[k] = datetime.datetime.fromtimestamp(int(v[6:]) / 1000)
        elif v[0:8] == '$isodate':
            try:
                dct[k] = dateutil.parser.parse(v[9:])
            except:
                continue
    return dct


def load_data(db, es, json_filepath):
    '''Bulk load from json into corresponding collections.
    Each item is expected to contain '_c' which represents the model class and the collection it belongs to.
    Validation rules are tested for each doc.
    '''

    docs_to_insert = []

    # the data will either come from MongoVue or mongoexport
    # mongoVue delimits each doc record with },{
    # mongoexport delimits each doc record with linefeed
    # let's find out which one it is by reading in file
    data = open(json_filepath).read()
    if re.search(r"\},\s*\{", data):
        # each doc is delimited with },{ like from MongoVue copy to clipboard
        clean_data = preparse_json_doc(data)
        # strip beginning {
        clean_data = re.sub(r"^(\s*\[\s*)*\s*\{\s*", "", clean_data)

        # strip ending
        clean_data = re.sub(r"\s*\}\s*(\s*\])*$", "", clean_data)

        docs = re.split(r"\},\s*\{", clean_data)
        for doc in docs:
            doc = doc.replace('\n', '')
            doc = "{" + doc + "}"
            doc = json.loads(doc, object_hook = mongo_json_object_hook)
            docs_to_insert.append(doc)
    else:
        # assume mongoexport with each doc on one line
        file = open(json_filepath)
        lines = [re.sub('\n', '', line) for line in filter(lambda a:(a != '\n'), file.readlines())]
        for line in lines:
            clean_line = preparse_json_doc(line)
            doc = json.loads(clean_line, object_hook = mongo_json_object_hook)
            docs_to_insert.append(doc)
        file.close()

    response = {}
    status = 200
    docs = []

    load_errors = []
    total_errors = 0
    total_added = 0

    for doc in docs_to_insert:
        class_id = doc['_c']
        model = getattr(models, class_id)
        collection_name = model.meta['collection']
        collection = db[collection_name]
        errors = {}

        # Validate
        doc_errors = validate(model, doc)
        if doc_errors:
            total_errors += doc_errors['count']
            load_errors.append(doc_errors)
            continue

        # init model for this doc
        initialized_model = model(**doc)

        #log date time user involved with this event
        # m.logit(user_id, 'post')

        # need to stuff into mongo
        doc_validated = initialized_model.to_python()

        dumped = bson_json_util.dumps(doc_validated)
        doc_info = {}
        doc_validated['_id'] = doc['_id']
        doc_validated['_id'] = collection.save(doc_validated, safe = True)
        # try to load generic display name used for indexing, etc
        try:
            doc_validated['dNam'] = initialized_model.dNam
        except:
            pass
        docs.append(doc_validated)

        ret = es.index(initialized_model.index, es.__dict__['index_name'], initialized_model._c, doc['_id'].__str__())

        total_added += 1

    response['total_inserted'] = len(docs)

    if load_errors:
        response['total_invalid'] = len(load_errors)
        response['errors'] = load_errors
        response['total_errors'] = total_errors
        status = 400
    else:
        response['total_invalid'] = 0


    response['docs'] = docs

    print "{count} docs loaded from: {json_filepath}!\n".format(count = total_added, json_filepath = json_filepath)

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

