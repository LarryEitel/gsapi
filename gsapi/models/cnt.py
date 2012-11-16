from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Tel, Im
from generic import FamTag, HobbyTag, SkillTag
from mixins import DxMixin

class Cnt(Mod, DxMixin):
    '''
    Google Contacts API: https://developers.google.com/google-apps/contacts/v3/
    '''
    code        = StringType(minimized_field_name='General Code', description='')

    # langs       = ListType(ModelType(Lang), minimized_field_name='Languages', description='Languages associated with this contact.')

    @property
    def index(self):
        return {
            "parsedtext": self.gatherKeywords(),
            "dNam"      : self.dNam,
            "dNamS"      : self.dNamS,
            "oOn"       : self.oOn
                }

    meta   = {
        'collection': 'cnts',
        '_c': 'Cnt',
        }
class Cmp(Cnt):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdOrganization'''
    # use dNam for company name from base Mod class
    # cNam = StringType(required=True, minimized_field_name='Company Name/Branch/Div/Department/Group/Troop', description='')
    # cNamS = StringType(required=True, minimized_field_name='Short Company Name', description='Abbreviation or Acronym')

    symbol = StringType(minimized_field_name='Company Symbol', description='')

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
    prefix    = StringType(minimized_field_name='Prefix', description='Examples: Mr, Mrs, Ms, etc')
    
    # givenName
    fNam      = StringType(minimized_field_name="First/Given Name")
    
    # additionalName
    fNam2     = StringType(minimized_field_name="Additional/Middle Name")
    
    # givenName
    lNam      = StringType(minimized_field_name="Family/Last Name")
    lNam2     = StringType()
    
    # nameSuffix
    suffix    = StringType(minimized_field_name='Suffix', description='Examples: MD, PHD, Jr, Sr, etc')
    gen       = StringType(minimized_field_name='Gender', choices=['m','f'], description='Gender')
    rBy       = ObjectIdType(minimized_field_name='Referred/Registered By', description='User that referred or registered this user.')
    
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

class Usr(Prs):
    root   = StringType(minimized_field_name='System Root User', description='a=Admin, m=Moderator')
    uNam   = StringType(required=True, minimized_field_name='UserName', description='')
    pw     = StringType(minimized_field_name='Password', description='Password Hash')
    # initially, this will contain 'admin' for admin users

    rstTkn = StringType(minimized_field_name='Reset Token', description='Used for resetting credentials.')
    rstOn  = DateTimeType(minimized_field_name='Reset Token DateTime Expiration', description='Used for resetting credentials.')

    lvOn   = DateTimeType(minimized_field_name='Last Viewed', description='DateTime when user last viewed the site.')

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
