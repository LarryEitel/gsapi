from schematics.types import IntType, LongType, StringType, DateTimeType
from schematics.types.compound import ListType, ModelType
from mod import Mod
from tag import Tag

# Event
# https://developers.google.com/gdata/docs/2.0/elements#gdEventKind


# ICalRecurrenceType()
# https://developers.google.com/gdata/docs/2.0/elements#gdRecurrence


# ICalRecurrenceExceptionType()
# https://developers.google.com/gdata/docs/2.0/elements#gdRecurrenceException

# ICalReminderType()
# https://developers.google.com/gdata/docs/2.0/elements#gdReminder


class Rdt(Mod):
    '''
        Robust datetime
        Date, given in format YYYY-MM-DD (with the year), or --MM-DD (without the year).
        Example:
            July 4, 1980: 
                1980-07-04
            December 13th, with no year specified: 
                '--12-13'
    '''
    # make yaml Rdt.log, Rdt.event, Rdt.todo, Rdt.anniverary, etc
    
    y            = IntType(minimized_field_name="Year", description="year ie, 2012")
    ym           = IntType(minimized_field_name="YearMonth", description="year+month, ie, 201207 or -60710")
    ymd          = IntType(minimized_field_name="YearMonthDay", description="year+month+day, ie, 20120730")
    isoDate      = StringType(minimized_field_name="Date in ISO", description="yyyymmdd")
    isoTime      = StringType(minimized_field_name="Time in ISO", description="hhss")
    tz           = StringType(minimized_field_name="Timezone ISO UTC", description="UTC in form of: [+-]hh:mm")
    
    instance     = StringType(minimized_field_name="Instance", description="b=begin, e=end, l=lap, m=milestone")
    period       = StringType(minimized_field_name="Period", description="b=before, a=after, c=circa/close")
    
    note         = StringType()
    
    valDelta0    = LongType() # in secs +/- year zero
    valDelta1970 = LongType() # in secs +/- year 1970

    @property
    def vValDelta1970(self):
        '''Generate datetime, delta 1970'''
        pass

    @property
    def vValDelta0(self):
        '''Generate datetime, delta 0'''
        pass

    @property
    def vDatetimeDelta1970(self):
        '''Generate datetime, delta 1970'''
        pass

    @property
    def vDatetimeDelta0(self):
        '''Generate datetime, delta 0'''
        pass

    # todo
    ''' create method to generate val based on supplied values'''
    meta                  = {
        '_c': 'Rdt',
        }
