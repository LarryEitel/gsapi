from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Phone, Im
from place import PlaceRel
class RoleType(Mod):
    '''
    type = StringType(enum) # j=job, f=family, fr=friend
    downName = StringType(default)
    upName = StringType() #optional
    '''
    meta = {
        'collection': 'roletypes',
        '_c': 'roletype',
        }
class RoleTitle(Mod):
    '''
    roleType_id = ObjectIdType()
    name = StringType()
    short = StringType()
    '''
    pass
class Role(_Model):
    '''
    type =
    roleType_id = ObjectId()
    title = StringType()
    permissions = ListType(['f', 'r'])
    #title_id = ObjectIdType()

    Examples
        Parent = Employer
        Child = Employee
        Mary is Employee of GSNI

    Mary and her Associations
        GSNI - Employer - Associate/Role
    '''

    meta = {
        'collection': 'roles',
        '_c': 'role',
        }

class CntXRel(Mod):
    '''Specifies the relationship between the containing entity and the contained person. '''
    name       = StringType(required=True, minimized_field_name='Relationship/Role', description='')
    nameShort  = StringType(minimized_field_name='Relationship/Role Short', description='')
    namePlural = StringType(minimized_field_name='Relationship/Role Plural', description='')
    weight     = StringType(minimized_field_name='Sort weight value', description='')
    mask       = StringType(minimized_field_name='Mask', description='ie. 1, 11')


company XYX
    bill supervisor for XYX 
    sue manager for XYX 

company ABC 
    sue owner of ABC

sue
    manager for XYZ
    owner of ABC

    supervisor OF company 
    supervisor OF company 

    dNam   = StringType(minimized_field_name="Display")
    dNamShort   = StringType(minimized_field_name="Display Short")


    @property
    def vNam(self):
        '''self.name + ', ' + self.mask'''
        pass

cntXRel = CntXRel(name=supervisor)

cntX = CntX(from_cnt, to_cnt, cntXRel)

class CntX(Mod):
    def __init__(self, from_cnt, to_cnt, cntXRel):
        super(CntX, self).__init__()
        self.from_cnt = from_cnt
        self.to_cnt = to_cnt
        self.cntXRel = cntXRel

    from_id = ObjectIdType(ObjectId)
    to_id   = ObjectIdType(ObjectId)
    rel_id  = ObjectIdType(ObjectId)

    relTitle = StringType(minimized_field_name='Role/relationship/job Title')
    relDesc = StringType(minimized_field_name='Role/relationship description, ie, Job Description.')
    weight  = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
    where  = StringType(minimized_field_name='Where', description='More location details.')

    dNam   = StringType(minimized_field_name="Display")
    dNamShort   = StringType(minimized_field_name="Display Short")


    Sitting on Bill_1_from
        to_Father of Sue_2_to
        Employer of Ted 


        Employee of ACME

    Sitting on Sue_2_from 
        from_Daughter of Bill_1_to


    @property
    def vNam(self):
        '''self.cntXRel.dNam + ' of ' + self.cnt.dNam'''
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




    '''primary key = cnt_id + rel_id '''

    meta = {
        'collection': 'cntxs',
        '_c': 'cntx',
        }
    meta = {
        'collection': 'cntxs',
        '_c': 'cntx',
        }

# class CntX(Mod):
#     def __init__(self, cnt, cntXRel):
#         super(CntX, self).__init__()
#         self.cnt_id = cnt._id
#         self.rel_id = cntXRel._id

#     relTitle = StringType(minimized_field_name='Role/relationship/job Title')
#     relDesc = StringType(minimized_field_name='Role/relationship description, ie, Job Description.')
#     weight  = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
#     where  = StringType(minimized_field_name='Where', description='More location details.')

#     dNam   = StringType(minimized_field_name="Display")
#     dNamShort   = StringType(minimized_field_name="Display Short")

#     @property
#     def vNam(self):
#         '''self.cntXRel.dNam + ' of ' + self.cnt.dNam'''
#         dNam = ''
#         fNam = ''
#         fNam += self.prefix + ' ' if self.prefix else ''
#         fNam += self.fNam + ' ' if self.fNam else ''
#         fNam += self.fNam2 + ' ' if self.fNam2 else ''
#         fNam = fNam[:-1] if fNam else ''

#         lNam = ''
#         lNam += self.lNam + ' ' if self.lNam else ''
#         lNam += self.lNam2 + ' ' if self.lNam2 else ''
#         lNam += self.suffix + ' ' if self.suffix else ''
#         lNam = lNam[:-1] if lNam else ''

#         if lNam:
#             dNam += lNam
#             if fNam:
#                 dNam += ', ' + fNam
#         elif fNam:
#             dNam += fNam
#         return dNam




#     '''primary key = cnt_id + rel_id '''

#     meta = {
#         'collection': 'cntxs',
#         '_c': 'cntx',
#         }
#     meta = {
#         'collection': 'cntxs',
#         '_c': 'cntx',
#         }

class Cnt(Mod):
    shares = ListType(ObjectIdType(ObjectId), minimized_field_name='Share List', description='List of Contacts shared with.')
    '''
    Google Contacts API: https://developers.google.com/google-apps/contacts/v3/
    '''
    code        = StringType(minimized_field_name='General Code', description='')

    tags        = ListType(StringType(minimized_field_name='Tags', description='General tags.'))
    # langs       = ListType(ModelType(Lang), minimized_field_name='Languages', description='Languages associated with this contact.')
    urls        = ListType(URLType(), minimized_field_name='Urls', description='Urls associated with this contact.')
    # imgs        = ListType(ModelType(Img), minimized_field_name='Images', description='Images associated with this contact.')
    phones      = ListType(ModelType(Phone), minimized_field_name='Phones', description='Phones associated with this contact.')
    emails      = ListType(ModelType(Email), minimized_field_name='Emails', description='Emails associated with this contact.')
    ims         = ListType(ModelType(Im), minimized_field_name='Instant Message Networks', description='')


    icon        = StringType(minimized_field_name='Place Icon', description='URL to an image resource that can be used to represent this Contact\'s type.')
    parents     = ListType(ModelType(CntX), minimized_field_name='Parents', description='')
    ancestors   = ListType(ModelType(CntX), minimized_field_name='Ancestors', description='')
    # events      = ListType(ModelType(Event), minimized_field_name='Ancestors', description='')
    placeRels   = ListType(ModelType(PlaceRel), minimized_field_name='Places', description='')
    descendants = ListType(ModelType(CntX), minimized_field_name='Descendants', description='')
    notes       = ListType(ModelType(Note), minimized_field_name='Notes', description='')

    meta   = {
        'collection': 'contacts',
        '_c': 'cnt',
        }
class Cmp(Cnt):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdOrganization'''
    cNam = StringType(required=True, minimized_field_name='Company Name/Branch/Div/Department/Group/Troop', description='')
    cNamShort = StringType(required=True, minimized_field_name='Short Company Name', description='Abbreviation or Acronym')

    symbol = StringType(minimized_field_name='Company Symbol', description='')
    type = StringType(minimized_field_name='Type of cNam.', choices=[
            'Branch',
            'Division',
            'ServiceArea',
            'ServiceUnit',
            'Department',
            'Group'
            'Troop'
            ],
        description='')

    meta = {
        'collection': 'contacts',
        '_c': 'cmp',
        }

    @property
    def index(self):
        return {
            "dNam"      : self.dNam,
            "oOn"       : self.oOn
                }

    @property
    def dNam(self):
        return self.cNam
class Prs(Cnt):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdName'''

    # namePrefix
    prefix = StringType(minimized_field_name='Prefix', description='Examples: Mr, Mrs, Ms, etc')

    # givenName
    fNam   = StringType(minimized_field_name="First/Given Name")

    # additionalName
    fNam2  = StringType(minimized_field_name="Additional/Middle Name")

    # givenName
    lNam   = StringType(minimized_field_name="Family/Last Name")
    lNam2  = StringType()

    # nameSuffix
    suffix = StringType(minimized_field_name='Suffix', description='Examples: MD, PHD, Jr, Sr, etc')
    gen     = StringType(minimized_field_name='Gender', choices=['m','f'], description='Gender')
    rBy     = ObjectIdType(minimized_field_name='Referred/Registered By', description='User that referred or registered this user.')

    dNam   = StringType(minimized_field_name="Display")
    dNamShort   = StringType(minimized_field_name="Display Short")

    meta = {
        'collection': 'contacts',
        '_c': 'Prs',
        }

    @property
    def index(self):
        return {
            "dNam"      : self.dNam,
            "oOn"       : self.oOn,
            "prefix"    : self.prefix
                }

    def save(self):
        pass

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
        '''Smith Sr, Mr Bill Wayne'''
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
    uNam   = StringType(required=True, minimized_field_name='UserName', description='')
    pw     = StringType(minimized_field_name='Password', description='Password Hash')
    # initially, this will contain 'admin' for admin users
    grps   = ListType(StringType(), minimized_field_name='Groups', description='List of Groups this Usr is a member of.')

    rstTkn = StringType(minimized_field_name='Reset Token', description='Used for resetting credentials.')
    rstOn  = DateTimeType(minimized_field_name='Reset Token DateTime Expiration', description='Used for resetting credentials.')

    lvOn   = DateTimeType(minimized_field_name='Last Viewed', description='DateTime when user last viewed the site.')

    meta   = {
        'collection': 'contacts',
        '_c': 'Usr',
        }

esCnt = {
    'parsedtext': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector" : "with_positions_offsets"},
    'dNam': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector" : "with_positions_offsets"},
    'title': {
        'boost': 1.0,
        'index': 'analyzed',
        'store': 'yes',
        'type': u'string',
        "term_vector" : "with_positions_offsets"},
    'oOn': {'store': 'yes',
        'type': 'date'},
    }
