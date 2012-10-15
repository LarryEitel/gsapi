from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, EmailType, FloatType

from schematics.types.mongo import ObjectIdType
from model import Mod

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
class Share(_Model):
    _c    = StringType(required=True, description='Class')
    _public_fields = ['_c']

    # The reason for this parent field given the fact that Wid'gets can contain an array of other widgets is that OTHER Widgets may LINK to this widget AND add their Share properties. It is necessary
    parent   = ObjectIdType(minimized_field_name='Parent Widget ID', description='Primary Parent owner of this widget.')

    usr_id   = ObjectIdType(minimized_field_name='Usr ID', description='Usr id for this Share.')

    permission   = StringType(minimized_field_name='Permission', choices=['aa','ab','b'], description='aa=At and Above, ab=At and below, b=Below.')


class Log(_Model):
    if 1: # Fields
        uNam  	= StringType()
        dt  	= DateTimeType()
        ip      = StringType()
        loc     = StringType()
        act  	= StringType(minimized_field_name='Action Name', description='')
        rs  	= StringType(minimized_field_name='Action Response', description='json blob related to return value of action')

    meta = {
        'collection': 'log',
        '_c': 'Log',
        }

class Email(_Model):
    if 1: # Fields
        email  = EmailType()
    	sort   = FloatType(minimized_field_name='Sort', description='Sorted with primary being first in list.')
    	note    = StringType()

    if 1: # Methods
        def __unicode__(self):
            return self.email

    meta = {
        'collection': 'contacts.emails',
        '_c': 'Eml',
        }
