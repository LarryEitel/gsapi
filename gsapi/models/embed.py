from schematics.models import Model as _Model
from mod import Mod
from schematics.types import StringType, IntType, DateTimeType, EmailType, FloatType, BooleanType, GeoPointType
from schematics.types.compound import ListType, ModelType
from schematics.types.mongo import ObjectIdType
from mod import Mod

# https://developers.google.com/gdata/docs/2.0/elements#gdMessageKind
class Msg(Mod):
    '''Represents a message, such as an email, a discussion group posting, or a comment.'''
    content = StringType()
    title   = StringType(description='Message subject.')
    geoPt   = GeoPointType(description='Geographic location the message was posted from.')

    meta = {
        '_c': 'Msg',
        }

class Shr(Mod):
    '''Share'''
    # The reason for this parent field given the fact that Wid'gets can contain an array of other widgets is that OTHER Widgets may LINK to this widget AND add their Share properties. It is necessary
    parId     = ObjectIdType(minimized_field_name='Parent Doc ID', description='Primary Parent owner of this doc.')
    
    # needed? Mod has oBy which is owner id
    usrId      = ObjectIdType(minimized_field_name='Usr ID', description='Usr id for this Share.')
    
    permission = StringType(minimized_field_name='Permission', choices=['a','ab','b'], description='a=At and Above, ab=At and below, b=Below.')

    meta = {
        '_c': 'Shr',
        }

class Email(Mod):
    address = EmailType(minimized_field_name='Email Address')

    w  = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
    
    prim    = BooleanType(default=False, minimized_field_name='Primary', description='When multiple emails appear in a list, indicates which is prim. At most one may be prim.')
    
    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'Email',
        }

class Tel(Mod):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdPhoneNumber'''
    if 1: # Fields
        address = EmailType(minimized_field_name='Email Address')
        
        w       = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
        lbl     = StringType(minimized_field_name='Label', description='A simple string value used to name this phone number. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')
        
        # enum  : home, work, other
        typs    = ListType(StringType(minimized_field_name='Telephone Types')
        
        uri     = StringType(minimized_field_name='An optional "tel URI"', description='An optional "tel URI" used to represent the number in a formal way, useful for programmatic access, such as a VoIP/PSTN bridge. See RFC 3966 for more information on tel URIs.')
        
        notes   = ListType(ModelType(Note))
        prim    = BooleanType(default=False, minimized_field_name='Primary', description='When multiple telephone numbers appear in a list, indicates which is prim. At most one may be prim.')
        
        # formatted_telephone_number
        dNam    = StringType(minimized_field_name='Display human readable form of telephone number.')

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'Tel',
        }

class Im(Mod):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdIm'''
    if 1: # Fields
        address  = StringType(minimized_field_name='IM Address')
        dNam     = StringType(minimized_field_name='Display Name', description='A display name of the entity (e.g. a person) the email address belongs to.')
        lbl      = StringType(minimized_field_name='Label', description='A simple string value used to name this IM address. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')
        w        = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
        
        # enum   : home, work, other
        typs     = ListType(StringType(minimized_field_name='IM Types')
        
        protocol = StringType(minimized_field_name='IM network', description='Identifies the IM network. The value may be either one of the standard values (shown below) or a URI identifying a proprietary IM network.')
        '''['aim','msn','yahoo','skype','qq','gtalk','icq','jabber']'''
        
        
        
        prim     = BooleanType(default=False, minimized_field_name='Primary', description='When multiple email extensions appear in a contact kind, indicates which is prim. At most one email may be prim.')
        notes    = ListType(ModelType(Note))

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'Im',
        }

class Note(Mod):
    title    = StringType()
    note     = StringType()
    noteHTML = StringType()

    def __unicode__(self):
        return self.note

    meta = {
        '_c': 'Note',
        }

class Rating(Mod):
    avg       = FloatType(description='Average rating.')
    max       = IntType(description='The rating scale\'s maximum value.')
    min       = IntType(description='The rating scale\'s minimum value.')
    numRaters = IntType(description='Number of ratings taken into account when computing the average value.')
    rel       = StringType(description='Specifies the aspect that\'s being rated. If not specified, the rating is an overall rating.')
    val       = IntType(description='Rating value.')

class PlAspectRating(_Model):
    typ       = StringType(minimized_field_name='Type', description='The name of the aspect that is being rated. eg. atmosphere, service, food, overall, etc.')
    rating    = Rating(minimized_field_name='Rating', description='The user\'s rating for this particular aspect')

    meta = {
        '_c': 'PlAspectRate',
        }

class Review(Mod):
    '''https://developers.google.com/maps/documentation/javascript/places#place_details_responses'''
    aspects = ListType(ModelType(PlaceAspectRating))
    cBy     = ObjectIdType(minimized_field_name='Author')
    body    = StringType(description='the user\'s review.')
    cOn     = DateTimeType(description='When Created/Added')

    meta = {
        '_c': 'Review',
        }
