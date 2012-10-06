from schematics.models import Model as _Model
from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from generic import Email


import datetime

class Mod(_Model):
    _c   = StringType(required=True, description='Class')
    _public_fields = ['_c']
    # owned
    oBy     = ObjectIdType()
    oOn     = DateTimeType() # ObjectIdType()
    oLoc    = StringType()
    
    # created
    cOn     = DateTimeType()
    cBy     = ObjectIdType()
    cLoc    = StringType()

    # modified
    mOn     = DateTimeType()
    mBy     = ObjectIdType()
    mLoc    = StringType()

    # deleted
    dele     = BooleanType(minimized_field_name='Deleted', description='Marked for removal.')
    dBy     = ObjectIdType()
    dOn     = DateTimeType()
    dLoc    = StringType()
    
    note    = StringType()

class Share(_Model):
    _c    = StringType(required=True, description='Class')
    _public_fields = ['_c']

    # The reason for this parent field given the fact that Wid'gets can contain an array of other widgets is that OTHER Widgets may LINK to this widget AND add their Share properties. It is necessary 
    parent   = ObjectIdType(minimized_field_name='Parent Widget ID', description='Primary Parent owner of this widget.')

    usr_id   = ObjectIdType(minimized_field_name='Usr ID', description='Usr id for this Share.')

    permission   = StringType(minimized_field_name='Permission', choices=['aa','ab','b'], description='aa=At and Above, ab=At and below, b=Below.')


class Wdg(Mod):
    _c    = StringType(required=True, description='Class')
    _public_fields = ['_c']
    name      = StringType()
    slug      = StringType(minimized_field_name='Slug', description='Used in URL params.')
    parents   = ObjectIdType(minimized_field_name='Parent Widget ID', description='Primary Parent owner of this widget.')
    ancestors = ListType(ObjectId, minimized_field_name='Ancestors', description='Ancestors of this widget.')
    children  = ListType(ModelType(Wid), minimized_field_name='Child Widgets', description='List of Wid(widgets) contained by this widget.')
    shares    = ListType(ModelType(Share), minimized_field_name='Share List', description='List of Cnts(contacts) this widget is shared with.')
    
    # Complete path to top parent of this thread (all ancestors)
    # FirstWidName/ChildOfFirstWidName/GrandChildOfFirstWidName
    dPath     = StringType()

    def gendPath(self):
        '''Walk up ancestors to generate a dPath'''
        pass

    @property
    def dNam(self):
        dNam = name

    meta   = {
        'collection': 'wids',
        '_c': 'wid',
        }

esCnt = {
    'parsedtext': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector" : "with_positions_offsets"},
    'dNam': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector" : "with_positions_offsets"},
    'title': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector" : "with_positions_offsets"}
    }
