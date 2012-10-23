from schematics.models import Model as _Model
from model import Mod
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, URLType
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

# add to widgets.py?
class Event(Wdg):
    '''https://developers.google.com/places/documentation/actions#event_details'''
    duration       = LongType(minimized_field_name='Duration', description="Duration in seconds.")

    # start_time
    begOn       = DateTimeType(minimized_field_name='Duration', description="Duration in seconds.")
    url         = URLType(minimized_field_name='Url', description="A URL pointing to details about the event.")
    summary     = StringType(minimized_field_name='Description', description="A textual description of the event. This property contains a string, the contents of which are not sanitized by the server. Your application should be prepared to prevent or deal with attempted exploits, if necessary.")

    meta   = {
        'collection': 'wdgs',
        '_c': 'event',
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
