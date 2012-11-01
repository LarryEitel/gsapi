from schematics.models import Model as _Model
from model import Mod
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from bson import ObjectId
from embed import Email, Note, Phone, Im, Share, Review

from schematics.types.mongo import ObjectIdType
from mixins import DxMixin

import datetime

class Wdg(Mod, DxMixind):
    slug      = StringType(minimized_field_name='Slug', description='Used in URL params.')

    @property
    def dNam(self):
        dNam = name

    meta   = {
        'collection': 'wdgs',
        '_c': 'wdg',
        }

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
