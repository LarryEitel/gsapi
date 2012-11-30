from schematics.models import Model as _Model
from schematics.types import StringType, IntType, LongType, DateTimeType, EmailType, FloatType, BooleanType, GeoPointType
from schematics.types.compound import ListType, ModelType
from schematics.types.mongo import ObjectIdType
from mod import Mod
from typ import Typ

class LnkTyp(Mod):
    fam         = BooleanType(description='Is Family Link/Relationship?')
    fr_c        = StringType(description='Fr/Child Document class "_c".')
    frGen       = StringType(description='Fr/Child Gender')
    frNam       = StringType(description='Fr/Child Name/Title')
    frNamS      = StringType(description='Fr/Child Name/Title Short')
    to_c        = StringType(description='To/Parent Document class "_c".')
    toGen       = StringType(description='To/Parent Gender')
    toNam       = StringType(description='To/Parent Name/Title')
    toNamS      = StringType(description='To/Parent Name/Title Short')
    mask        = StringType(description='Sharing Mask')
    '''1, 11, 111, etc used in sh(aring) docs'''

class Lnk(Mod):
    eId         = IntType(description='Element Id')
    d_c         = StringType(description='Document class "_c".')
    dId         = LongType(description='Document Id.')
    lnkTypDNam  = LongType(description='Link Type Display Name')
    lnkTypDNamS = LongType(description='Link Type Display Name Short')
    dDNam       = LongType(description='Document Display Name')
    sDNamS      = LongType(description='Document Display Name Short')

class Pth(Mod):
    eId         = IntType(description='Element Id')
    d_c      = StringType(description='Target document class "_c".')
    dId      = LongType(description='Target document Id.')
    lnkTypId = LongType(description='Link Type Id.')
    lnkTitle = StringType(description='Link Title.')
    lnkNote  = StringType(description='Link Note.')
    lnks     = ListType(ModelType(Lnk))
    ids      = ListType(LongType())

class Note(Mod):
    eId      = IntType(description='Element Id')
    title    = StringType()
    note     = StringType()
    noteHTML = StringType()

    def __unicode__(self):
        return self.note

    meta = {
        '_c': 'Note',
        }

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
    parId     = ObjectIdType(description='Parent Doc ID, Primary Parent owner of this doc.')
    
    # needed? Mod has oBy which is owner id
    usrId      = ObjectIdType(description='Usr ID for this Share.')
    
    permission = StringType(description='Permission, a=At and Above, ab=At and below, b=Below.', choices=['a','ab','b'])

    meta = {
        '_c': 'Shr',
        }

class Email(Mod):
    typ     = StringType() 
    '''typ.work'''
    eId     = IntType(required=True, description='Element Id')
    address = EmailType(required=True, description='Email Address')
    w       = FloatType(description='Sort weight, Sort list by weight value.', default=0)
    
    prim    = BooleanType(default=False, description='Primary, When multiple emails appear in a list, indicates which is prim. At most one may be prim.')

    meta = {
        '_c': 'Email',
        }

    @property
    def vNam(self):
        dNam = self.typ['dNam'] + ': ' + self.address.lower()
        dNam += '(Primary)' if self.prim else ''
        return dNam

    @property
    def vNamS(self):
        return self.dNam.lower().replace(' ', '_')

    class Meta:
        mixin = True

class Tel(Mod):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdPhoneNumber'''
    if 1: # Fields
        eId         = IntType(description='Element Id')
        address = EmailType(description='Email Address')
        
        w       = FloatType(description='Sort weight, Sort list by weight value.')
        lbl     = StringType(description='Label, A simple string value used to name this phone number. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')
        
        # enum  : home, work, other
        typs    = ListType(StringType(description='Telephone Types'))
        
        uri     = StringType(description='An optional "tel URI", An optional "tel URI" used to represent the number in a formal way, useful for programmatic access, such as a VoIP/PSTN bridge. See RFC 3966 for more information on tel URIs.')
        
        notes   = ListType(ModelType(Note))
        prim    = BooleanType(default=False, description='Primary, When multiple telephone numbers appear in a list, indicates which is prim. At most one may be prim.')
        
        # formatted_telephone_number
        dNam    = StringType(description='Display human readable form of telephone number.')

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'Tel',
        }

class Im(Mod):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdIm'''
    if 1: # Fields
        eId         = IntType(description='Element Id')
        address  = StringType(description='IM Address')
        dNam     = StringType(description='Display Name, A display name of the entity (e.g. a person) the email address belongs to.')
        lbl      = StringType(description='Label, A simple string value used to name this IM address. It allows UIs to display a label such as "Work", "Personal", "Preferred", etc.')
        w        = FloatType(description='Sort weight, Sort list by weight value.')
        
        # enum   : home, work, other
        typs     = ListType(StringType(description='IM Types'))
        
        protocol = StringType(description='IM network, Identifies the IM network. The value may be either one of the standard values (shown below) or a URI identifying a proprietary IM network.')
        '''['aim','msn','yahoo','skype','qq','gtalk','icq','jabber']'''
        
        
        
        prim     = BooleanType(default=False, description='Primary, When multiple email extensions appear in a contact kind, indicates which is prim. At most one email may be prim.')
        notes    = ListType(ModelType(Note))

    if 1: # Methods
        def __unicode__(self):
            return self.address

    meta = {
        '_c': 'Im',
        }

class Rating(Mod):
    eId       = IntType(description='Element Id')
    avg       = FloatType(description='Average rating.')
    max       = IntType(description='The rating scale\'s maximum value.')
    min       = IntType(description='The rating scale\'s minimum value.')
    numRaters = IntType(description='Number of ratings taken into account when computing the average value.')
    rel       = StringType(description='Specifies the aspect that\'s being rated. If not specified, the rating is an overall rating.')
    val       = IntType(description='Rating value.')

class PlAspectRating(_Model):
    typ       = StringType(description='Type, The name of the aspect that is being rated. eg. atmosphere, service, food, overall, etc.')
    rating    = Rating(description='Rating, The user\'s rating for this particular aspect')

    meta = {
        '_c': 'PlAspectRate',
        }

class Review(Mod):
    '''https://developers.google.com/maps/documentation/javascript/places#place_details_responses'''
    eId     = IntType(description='Element Id')
    aspects = ListType(ModelType(PlAspectRating))
    cBy     = ObjectIdType(description='Author')
    body    = StringType(description='the user\'s review.')
    cOn     = DateTimeType(description='When Created/Added')

    meta = {
        '_c': 'Review',
        }
