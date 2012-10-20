from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType
from schematics.types.compound import ListType, ModelType

# Event
# https://developers.google.com/gdata/docs/2.0/elements#gdEventKind


# ICalRecurrenceType()
# https://developers.google.com/gdata/docs/2.0/elements#gdRecurrence


# ICalRecurrenceExceptionType()
# https://developers.google.com/gdata/docs/2.0/elements#gdRecurrenceException

# ICalReminderType()
# https://developers.google.com/gdata/docs/2.0/elements#gdReminder

# add to widgets.py?
class Event(_Model):
    '''https://developers.google.com/places/documentation/actions#event_details'''
    duration       = LongType(description='Duration', description="Duration in seconds.")

    # start_time
    begOn       = DateTimeType(description='Duration', description="Duration in seconds.")
    url         = URLType(description='Url', description="A URL pointing to details about the event.")
    summary     = StringType(description='Description', description="A textual description of the event. This property contains a string, the contents of which are not sanitized by the server. Your application should be prepared to prevent or deal with attempted exploits, if necessary.")

class When(_Model):
    '''
        Date, given in format YYYY-MM-DD (with the year), or --MM-DD (without the year).
        Example:
            July 4, 1980: 
                1980-07-04
            December 13th, with no year specified: 
                '--12-13'
    '''
    val     = StringType()
    meta = {
        '_c': 'when',
        }


class On(_Model):
    '''
        Date, given in format YYYY-MM-DD (with the year), or --MM-DD (without the year).
        Example:
            July 4, 1980: 
                1980-07-04
            December 13th, with no year specified: 
                '--12-13'
    '''
    typeId  : String # enum l=log, e=event, t=todo, a=anniverary
    beg_end_lap_milestone : b or e
    tags    : [String] # DS=Discussion, CALL, wedding, hired, etc
    y       : Number # year ie, 2012
    ym      : Number # year+month, ie, 201207 or -60710
    ymd     : Number # year+month+day, ie, 20120730
    datetime: Date
    is      : String # enum: b=before, a=after, c=circa/close
    note    : String
    dNam    : Display version (c)2012
    dNamShort : dNam Short

    val     = StringType()
    meta = {
        '_c': 'when',
        }
