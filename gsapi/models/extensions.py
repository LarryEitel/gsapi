from schematics.base import ModelException
#from flaskext.mail import Mail

#db = PyMongo
#mail = Mail()

from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]



def validate(model, doc):
    '''Validate all fields. Return any/all failed validation along with details'''

    errors = []

    try:
        model(**doc).validate(validate_all=True)
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
