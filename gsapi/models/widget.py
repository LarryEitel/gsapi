from schematics.models import Model as _Model
from model import Mod
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Phone, Im, Share, Review
from place import PlaceRel

import datetime


class Wdg(Mod):
    name      = StringType()
    nameShort = StringType()
    slug      = StringType(minimized_field_name='Slug', description='Used in URL params.')
    shares    = ListType(ModelType(Share), minimized_field_name='Share List', description='List of Cnts(contacts) this widget is shared with.')
    followers = ListType(ObjectIdType(ObjectId), minimized_field_name='Followers', description='Followers of this widget.')
    parents   = ObjectIdType(minimized_field_name='Parent Widget ID', description='Parent owner of this widget.')
    ancestors = ListType(ObjectIdType(ObjectId), minimized_field_name='Ancestors', description='Ancestors of this widget.')
    children  = ListType(ObjectIdType(ObjectId), minimized_field_name='Child Widgets', description='List of Wid(widgets) contained by this widget.')
    

    rating     = IntType(minimized_field_name='Rating', description='')
    reviews    = ListType(ModelType(Review))
        

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
        'collection': 'wdgs',
        '_c': 'wdg',
        }

esWdg = {
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
