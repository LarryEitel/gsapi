from schematics.models import Model
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



class Log(Model):
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

class Email(Model):
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
