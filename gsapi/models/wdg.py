from schematics.models import Model as _Model
from mod import Mod
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from bson import ObjectId
from embed import Email, Note, Im, Shr, Review

from schematics.types.mongo import ObjectIdType
from mixins import ModMixin

import datetime

class Wdg(Mod, ModMixin):
    slug      = StringType(description='Slug Used in URL params.')

    @property
    def dNam(self):
        dNam = name

    meta   = {
        'collection': 'wdgs',
        '_c': 'Wdg',
        }

class Event(Wdg):
    '''https://developers.google.com/places/documentation/actions#event_details'''
    duration       = LongType(description="Duration in seconds.")

    # start_time
    begOn       = DateTimeType(description="Duration Duration in seconds.")
    url         = URLType(description="A URL pointing to details about the event.")
    summary     = StringType(description="A textual description of the event. This property contains a string, the contents of which are not sanitized by the server. Your application should be prepared to prevent or deal with attempted exploits, if necessary.")

    meta   = {
        'collection': 'wdgs',
        '_c': 'Event',
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
