from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from generic import Email

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
class CntX(Mod):
    cnt_id = ObjectIdType(ObjectId)
    role_id = ObjectIdType(ObjectId)
    weight = FloatType()

    '''primary key = cnt_id + role_id '''

    meta = {
        'collection': 'contactxs',
        '_c': 'cntx',
        }

class Cnt(Mod):
    shares = ListType(ObjectIdType(ObjectId), minimized_field_name='Share List', description='List of Contacts shared with.')
    emails = ListType(ModelType(Email), minimized_field_name='Emails', description='Email addresses.')
    cntXs = ListType(ModelType(CntX), minimized_field_name='Associations', description='Associations')
    meta   = {
        'collection': 'contacts',
        '_c': 'cnt',
        }


class Cmp(Cnt):
    cNam = StringType(required=True, minimized_field_name='Company Name', description='')

    meta = {
        'collection': 'contacts',
        '_c': 'cmp',
        }

    @property
    def dNam(self):
        return self.cNam

class Prs(Cnt):
    title  = StringType(minimized_field_name='Title', description='Examples: Mr, Mrs, Ms, etc')
    fNam   = StringType() #max_length=4
    fNam2  = StringType()
    lNam   = StringType()
    lNam2  = StringType()
    suffix = StringType(minimized_field_name='Suffix', description='Examples: MD, PHD, Jr, Sr, etc')
    gen     = StringType(minimized_field_name='Gender', choices=['m','f'], description='Gender')
    rBy     = ObjectIdType(minimized_field_name='Referred/Registered By', description='User that referred or registered this user.')

    meta = {
        'collection': 'contacts',
        '_c': 'Prs',
        }

    def save(self):
        pass

    @property
    def dNam(self):
        dNam = ''
        fNam = ''
        fNam += self.title + ' ' if self.title else ''
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

    # def onUpdate(self):
    #     super(Prs, self).onUpdate()


class Usr(Prs):
    uNam         = StringType(required=True, minimized_field_name='UserName', description='')
    pw           = StringType(minimized_field_name='Password', description='')
    # initially, this will contain 'admin' for admin users
    groups       = ListType(StringType(), minimized_field_name='User Groups', description='List of Groups this Usr is a member of.')
    lvOn         = DateTimeType(minimized_field_name='Last Viewed', description='DateTime when user last viewed the site.')

    meta = {
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
        "term_vector" : "with_positions_offsets"}
    }
