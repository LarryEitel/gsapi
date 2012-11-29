from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Tel, Im
from mixins import ModMixin

# class Cnt(Mod, ModMixin):
class Cnt(Mod):
    '''
    Google Contacts API: https://developers.google.com/google-apps/contacts/v3/
    '''
    code        = StringType(description='')

    # langs       = ListType(ModelType(Lang), description='Languages associated with this contact.')

    @property
    def index(self):
        return {
            "parsedtext": self.gatherKeywords(),
            "dNam"      : self.dNam,
            "dNamS"     : self.dNamS,
            "oOn"       : self.oOn
                }

    meta   = {
        'collection': 'cnts',
        '_c': 'Cnt',
        }
class Cmp(Cnt):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdOrganization'''
    # use dNam for company name from base Mod class
    # cNam = StringType(required=True, description='')
    # cNamS = StringType(required=True, description='Abbreviation or Acronym')

    symbol = StringType(description='')

    meta = {
        'collection': 'cnts',
        '_c': 'Cmp',
        }

    @property
    def index(self):
        return {
            "symbol"    : self.symbol,
                }

    @property
    def vNam(self):
        return self.cNam
class Prs(Cnt):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdName'''

    # namePrefix
    prefix    = StringType(description='Examples: Mr, Mrs, Ms, etc')
    
    # givenName
    fNam      = StringType()
    
    # additionalName
    fNam2     = StringType()
    
    # givenName
    lNam      = StringType()
    lNam2     = StringType()
    
    # nameSuffix
    suffix    = StringType(description='Examples: MD, PHD, Jr, Sr, etc')
    gen       = StringType(choices=['m','f'], description='Gender')
    rBy       = ObjectIdType(description='User that referred or registered this user.')
    
    meta      = {
        'collection': 'cnts',
        '_c'        : 'Prs',
        }

    @property
    def index(self):
        return {
            "dNam"      : self.dNam,
            "oOn"       : self.oOn,
                }

    @property
    def fullName(self):
        '''Mr Bill Wayne Smith Sr'''
        dNam = ''
        fNam = ''
        fNam += self.prefix + ' ' if self.prefix else ''
        fNam += self.fNam + ' ' if self.fNam else ''
        fNam += self.fNam2 + ' ' if self.fNam2 else ''
        fNam = fNam[:-1] if fNam else ''

        lNam = ''
        lNam += self.lNam + ' ' if self.lNam else ''
        lNam += self.lNam2 + ' ' if self.lNam2 else ''
        lNam += self.suffix + ' ' if self.suffix else ''
        lNam = lNam[:-1] if lNam else ''

        return fNam + (' ' + lNam if lNam else '')

        
    @property
    def vNam(self):
        '''Generate dNam, ie, Smith Sr, Mr Bill Wayne'''
        dNam = ''
        fNam = ''
        fNam += self.prefix + ' ' if self.prefix else ''
        fNam += self.fNam + ' ' if self.fNam else ''
        fNam += self.fNam2 + ' ' if self.fNam2 else ''
        fNam = fNam[:-1] if fNam else ''

        lNam = ''
        lNam += self.lNam + ' ' if self.lNam else ''
        lNam += self.lNam2 + ' ' if self.lNam2 else ''
        lNam += self.suffix + ' ' if self.suffix else ''
        lNam = lNam[:-1] if lNam else ''

        if lNam:
            dNam += lNam
            if fNam:
                dNam += ', ' + fNam
        elif fNam:
            dNam += fNam
        return dNam

    @property
    def vNamS(self):
        return self.dNam.lower().replace(' ', '_')

class Usr(Prs):
    root   = StringType(description='a=Admin, m=Moderator')
    uNam   = StringType(required=True, description='')
    pw     = StringType(description='Password Hash')
    # initially, this will contain 'admin' for admin users

    rstTkn = StringType(description='Used for resetting credentials.')
    rstOn  = DateTimeType(description='Used for resetting credentials.')

    lvOn   = DateTimeType(description='DateTime when user last viewed the site.')

    meta   = {
        'collection': 'cnts',
        '_c': 'Usr',
        }

# esCnt = {
#     'parsedtext': {
#         'boost': 1.0,
#         'index': 'analyzed',
#         'store': 'yes',
#         'type': u'string',
#         "term_vector" : "with_positions_offsets"},
#     'dNam': {
#         'boost': 1.0,
#         'index': 'analyzed',
#         'store': 'yes',
#         'type': u'string',
#         "term_vector" : "with_positions_offsets"},
#     'oOn': {'store': 'yes',
#         'type': 'date'},
#     }
