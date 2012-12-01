from schematics.base import ModelException
from schematics.validation import validate_instance, validate_class_partial
#from flaskext.mail import Mail

#db = PyMongo
#mail = Mail()

from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

        
def nextEId(doc, attrNam):
    '''Get next element eId for a list item'''
    
    # if doc['eIds'] doesn't exist, add it
    if not 'eIds' in doc:
        doc['eIds'] = {}
        
    # if doc['eIds']['attrNam'] does not exist, add it and return 1
    if not attrNam in doc['eIds']:
        doc['eIds'][attrNam] = 2
        return {'doc': doc, 'eId': 1}
    else:
        eId = doc['eIds'][attrNam]
        doc['eIds'][attrNam] += 1
        return {'doc': doc, 'eId': eId}
        

def doc_remove_empty_keys(doc):
    '''Remove any dict keys without a value'''
    doc_clean       = {}
    for k, v in doc.iteritems():
        if doc[k]:
            doc_clean[k] = doc[k]
            
    return doc_clean

def validate_partial(model, patch):
    '''Validate only fields submitted. Return any/all failed validation along with details'''

    errors = []

    try:
        validate_class_partial(model, patch)
        # model(**doc).validate(validate_all=True)
    except ModelException, errs:
        for err in errs.error_list:
            errors.append(err.__dict__)

    return {'patch':patch, 'errors':errors, 'count':len(errors)} if errors else None



def validate(model, doc):
    '''Validate all fields. Return any/all failed validation along with details'''

    errors = []

    try:
        validate_instance(model(**doc))
        # model(**doc).validate(validate_all=True)
    except ModelException, errs:
        for err in errs.error_list:
            errors.append(err.__dict__)

    return {'doc':doc, 'errors':errors, 'count':len(errors)} if errors else None




# def validate(model, doc):
#     '''Validate all fields. Return any/all failed validation along with details'''
#     errors = []
#     src_doc = copy.deepcopy(doc)

#     while True:
#         try:
#             model(**doc).validate()
#             break
#         except TypeException, se:
#             error                = {}
#             details              = se.__dict__
#             field_name           = details['field_name']
#             field_value          = details['field_value']
#             reason               = details['reason']
            
#             # remove failed field so we can validate the remaining fields
#             del(doc[field_name])
#             error['field_name']  = field_name
#             error['field_value'] = field_value
#             error['reason']      = reason
#             errors.append(error)

#     return {'doc':src_doc, 'errors':errors, 'count':len(errors)} if errors else None
