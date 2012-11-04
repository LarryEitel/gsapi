from schematics.models import Model as _Model
from model import Mod
from schematics.types import StringType, IntType, DateTimeType, EmailType, FloatType, BooleanType, GeoPointType
from schematics.types.compound import ListType, ModelType
from schematics.types.mongo import ObjectIdType
from model import Mod

# https://developers.google.com/gdata/docs/2.0/elements#gdMessageKind
class Message(Mod):
    '''Represents a message, such as an email, a discussion group posting, or a comment.'''
    tags        = ListType(StringType())
    content     = StringType()
    title       = StringType(description='Message subject.')
    geoPt       = GeoPointType(description='Geographic location the message was posted from.')

class Shr(Mod):
    '''Share'''
    # The reason for this parent field given the fact that Wid'gets can contain an array of other widgets is that OTHER Widgets may LINK to this widget AND add their Share properties. It is necessary
    parent   = ObjectIdType(minimized_field_name='Parent Widget ID', description='Primary Parent owner of this widget.')

    usrId   = ObjectIdType(minimized_field_name='Usr ID', description='Usr id for this Share.')

    permission   = StringType(minimized_field_name='Permission', choices=['aa','ab','b'], description='aa=At and Above, ab=At and below, b=Below.')

class Email(_Model):
    address = EmailType(minimized_field_name='Email Address')
    dNam    = StringType(minimized_field_name='Display Name', description='A display name of the entity (e.g. a person) the email address belongs to.')
    weight  = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
    lbl   = StringType(minimized_field_name='Label', description='A simple string value used to name this email address. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')

    # enum: home, work, other
    rel     = StringType(minimized_field_name='Type of email', description='A programmatic value that identifies the type of email')

    primary = BooleanType(default=False, minimized_field_name='Primary', description='When multiple emails appear in a list, indicates which is primary. At most one may be primary.')
    note    = StringType()

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'email',
        }

class Tel(_Model):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdPhoneNumber'''
    if 1: # Fields
        address = EmailType(minimized_field_name='Email Address')
        weight  = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
        label   = StringType(minimized_field_name='Label', description='A simple string value used to name this phone number. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')

        # enum: home, work, other
        rel     = StringType(minimized_field_name='Type of phone', description='A programmatic value that identifies the type of phone')
        uri     = StringType(minimized_field_name='An optional "tel URI"', description='An optional "tel URI" used to represent the number in a formal way, useful for programmatic access, such as a VoIP/PSTN bridge. See RFC 3966 for more information on tel URIs.')

        note    = StringType()
        primary = BooleanType(default=False, minimized_field_name='Primary', description='When multiple phone numbers appear in a list, indicates which is primary. At most one may be primary.')

        # formatted_phone_number
        dNam    = StringType(minimized_field_name='Display human readable form of phone number.')

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'email',
        }

class Im(_Model):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdIm'''
    if 1: # Fields
        address = StringType(minimized_field_name='IM Address')
        dNam    = StringType(minimized_field_name='Display Name', description='A display name of the entity (e.g. a person) the email address belongs to.')
        label   = StringType(minimized_field_name='Label', description='A simple string value used to name this IM address. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')
        weight  = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')

        # enum: home, work, other
        rel     = StringType(minimized_field_name='Type of IM', description='A programmatic value that identifies the type of IM')

        protocol= StringType(minimized_field_name='IM network', description='Identifies the IM network. The value may be either one of the standard values (shown below) or a URI identifying a proprietary IM network.')
        '''['aim','msn','yahoo','skype','qq','gtalk','icq','jabber']'''



        primary = BooleanType(default=False, minimized_field_name='Primary', description='When multiple email extensions appear in a contact kind, indicates which is primary. At most one email may be primary.')
        note    = StringType()

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'im',
        }

class Note(_Model):

    note    = StringType()

    def __unicode__(self):
        return self.note

    meta = {
        '_c': 'note',
        }

class Rating(_Model):
    average     = FloatType(description='Average rating.')
    max         = IntType(description='The rating scale\'s maximum value.')
    min         = IntType(description='The rating scale\'s minimum value.')
    numRaters   = IntType(description='Number of ratings taken into account when computing the average value.')
    rel         = StringType(description='Specifies the aspect that\'s being rated. If not specified, the rating is an overall rating.')
    value       = IntType(description='Rating value.')

class PlAspectRating(_Model):
    type      = StringType(minimized_field_name='Type', description='The name of the aspect that is being rated. eg. atmosphere, service, food, overall, etc.')
    rating    = Rating(minimized_field_name='Rating', description='The user\'s rating for this particular aspect')

    meta = {
        '_c': 'placeaspectrate',
        }

class Review(_Model):
    '''https://developers.google.com/maps/documentation/javascript/places#place_details_responses'''
    aspects      = ListType(ModelType(PlaceAspectRating))
    author       = ObjectIdType()
    body         = StringType(description='the user\'s review.')
    addedOn      = DateTimeType(description='When Added')

    meta = {
        '_c': 'review',
        }
