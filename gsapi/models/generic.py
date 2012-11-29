from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, EmailType, FloatType

from schematics.types.mongo import ObjectIdType
from mod import Mod
from embed import Note

class AppId(Mod):
    appName  = StringType()
    appKey   = StringType()
    appId    = StringType()
    appUrl   = StringType()
    siteUrl  = StringType()
    callBack = StringType()

    meta   = {
        'collection': 'apps',
        '_c': 'AppId',
    }
# class Share(_Model):
#     _c    = StringType(required=True, description='Class')
#     _public_fields = ['_c']

#     # The reason for this parent field given the fact that Wid'gets can contain an array of other widgets is that OTHER Widgets may LINK to this widget AND add their Share properties. It is necessary
#     parent   = ObjectIdType(description='Parent Widget ID', description='Primary Parent owner of this widget.')

#     usr_id   = ObjectIdType(description='Usr ID', description='Usr id for this Share.')

#     permission   = StringType(description='Permission', choices=['aa','ab','b'], description='aa=At and Above, ab=At and below, b=Below.')


class Log(_Model):
    if 1: # Fields
        uNam  	= StringType()
        dt  	= DateTimeType()
        ip      = StringType()
        loc     = StringType()
        act  	= StringType(description='Action Name')
        rs  	= StringType(description='Action Response, json blob related to return value of action')

    meta = {
        'collection': 'log',
        '_c': 'Log',
    }

# class Email(_Model):
#     if 1: # Fields
#         email  = EmailType()
#     	sort   = FloatType(description='Sort', description='Sorted with prim being first in list.')
#     	note    = StringType()

#     if 1: # Methods
#         def __unicode__(self):
#             return self.email

#     meta = {
#         'collection': 'contacts.emails',
#         '_c': 'Eml',
#         }

# class Note(_Model):

#     if 1: # Fields
#         note    = StringType()

#     if 1: # Methods
#         def __unicode__(self):
#             return self.note

#     meta = {
#         '_c': 'note',
#         }