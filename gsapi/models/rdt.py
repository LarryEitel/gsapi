from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType
from schematics.types.compound import ListType, ModelType

# Event
# https://developers.google.com/gdata/docs/2.0/elements#gdEventKind


# ICalRecurrenceType()
# https://developers.google.com/gdata/docs/2.0/elements#gdRecurrence


# ICalRecurrenceExceptionType()
# https://developers.google.com/gdata/docs/2.0/elements#gdRecurrenceException

# ICalReminderType()
# https://developers.google.com/gdata/docs/2.0/elements#gdReminder


class Rdt(_Model):
    '''
        Date, given in format YYYY-MM-DD (with the year), or --MM-DD (without the year).
        Example:
            July 4, 1980: 
                1980-07-04
            December 13th, with no year specified: 
                '--12-13'
    '''
    # typId                = StringType(minimized_field_name="Type", description="l=log, e=event, t=todo, a=anniverary")
    typId = StringType(minimized_field_name="Begin/End/Lap/Mileston", description="b=begin, e=end, l=lap, m=milestone")
    tags                  = ListType(StringType(minimized_field_name='Tags', description='General tags.'))
    y                     = IntType(minimized_field_name="Year", description="year ie, 2012")
    ym                    = IntType(minimized_field_name="YearMonth", description="year+month, ie, 201207 or -60710")
    ymd                   = IntType(minimized_field_name="YearMonthDay", description="year+month+day, ie, 20120730")
    datetime              = DateTimeType()
    when                  = StringType(minimized_field_name="When", description="b=before, a=after, c=circa/close")
    note                  = StringType()
    dNam                  = StringType(minimized_field_name="Display Verbose", description="Display version (c)2012")
    dNamS             = StringType(minimized_field_name="Display Short", description="")
    
    val                   = LongType()
    meta                  = {
        '_c': 'on',
        }
