from schematics.models import Model
from schematics.types import StringType, DateTimeType, EmailType

class Email(Model):
    if 1: # Fields
        email  = EmailType()
    if 1: # Methods
        def __unicode__(self):
            return self.email

    meta = {
        'collection': 'contacts.emails',
        '_c': 'Eml',
        }
