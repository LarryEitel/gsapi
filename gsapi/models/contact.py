from model import Mod
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from generic import Email

class Cnt(Mod):
    shares = ListType(ObjectIdType(ObjectId), minimized_field_name='Share List', description='List of Contacts shared with.')
    emails = ListType(ModelType(Email), minimized_field_name='Emails', description='Email addresses.')
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


# sample
# add field like: testVal = StringType(validation=testvalidation)
# def testvalidation(val):
#     print val
#     return True


# class Person(Contact):
#     title  = StringType(minimized_field_name='Title', description='Examples: Mr, Mrs, Ms, etc')
#     fNam   = StringType() #max_length=4
#     fNam2  = StringType()
#     lNam   = StringType()
#     lNam2  = StringType()
#     suffix = StringType(minimized_field_name='Suffix', description='Examples: MD, PHD, Jr, Sr, etc')
#     gen     = StringType(minimized_field_name='Gender', choices=['m','f'], description='Gender')
#     rBy     = ObjectIdType(minimized_field_name='Referred/Registered By', description='User that referred or registered this user.')

#     meta = {
#         'collection': 'contacts',
#         '_c': 'prs',
#         }

#     @property
#     def dNam(self):
#         return 'hello'

#     def onUpdate(self):
#         super(Person, self).onUpdate()
#         dnam = ''
#         fNam = ''
#         fNam += self.title + ' ' if self.title else ''
#         fNam += self.fNam + ' ' if self.fNam else ''
#         fNam += self.fNam2 + ' ' if self.fNam2 else ''
#         fNam = fNam[:-1] if fNam else ''

#         lNam = ''
#         lNam += self.lNam + ' ' if self.lNam else ''
#         lNam += self.lNam2 + ' ' if self.lNam2 else ''
#         lNam += self.suffix + ' ' if self.suffix else ''
#         lNam = lNam[:-1] if lNam else ''

#         if lNam:
#             dnam += lNam
#             if fNam:
#                 dnam += ', ' + fNam
#         elif fNam:
#             dnam += fNam
#         self.dnam = dnam



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

    @property
    def dNam(self):
        return 'hello'

    def onUpdate(self):
        super(Prs, self).onUpdate()
        dnam = ''
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
            dnam += lNam
            if fNam:
                dnam += ', ' + fNam
        elif fNam:
            dnam += fNam
        self.dnam = dnam

    
class Usr(Prs):
    unam         = StringType(minimized_field_name='UserName', description='')
    lvOn         = DateTimeType(minimized_field_name='Last Viewed', description='DataTime when user last viewed the site.')

    meta = {
        'collection': 'contacts',
        '_c': 'usr',
        }

