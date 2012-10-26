from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Phone, Im

class RelToFr(_Model):
    '''To/Parent/Target/From/Child relationship details which are embedded into a ListType named tos or frm.
        NOTE:
            Accomodate access/visibility controls? If target (rel)ationship is not viewable based on share options, then user should not see this relationship in list. Right?
        ''' 
    docID        = ObjectIdType(ObjectId)
    docC         = ObjectIdType(ObjectId)
    relDNam      = StringType(minimized_field_name="Relation/Role")
    relDNamShort = StringType(minimized_field_name="Relation/Role Short")
    docDNam      = StringType(minimized_field_name="Doc Display Name")
    docDNamShort = StringType(minimized_field_name="Doc Display Name Short")

class Rel(_Model):
    # In a list of (rel)ationships, ie, Companies (cmp), Persons (prs), Places (pl), Events (ev), etc, docC = the class so that client can retrieve place (rel)ationships for example.
    # this docC is the doc Class of the immediate parent which exists/occurs last in the array/list of IDs/relToFrs
    docC         = ObjectIdType(ObjectId)

    # List of Doc IDs in the relToFms list. This is used to quickly check whether a doc ID is referenced.
    # This should be reviewed for effeciency
    IDs   = ListType(ObjectIdType(ObjectId))

    # List of (rel)ationship details
    relToFrs = ListType(ModelType(RelToFm))
    
    # in a list of aPath's, sort list on this value to control order
    weight    = FloatType(minimized_field_name='Sort weight value', description='')


class DxRel(Mod):
    '''Specifies the relationship between document objects. '''
    frC    = StringType(minimized_field_name='From/Subject Class', description='')    
    frNam  = StringType(minimized_field_name='From Relationship/Role', description='')
    frGen  = StringType(minimized_field_name='From/Subject Gender', description='')
    
    toC    = StringType(minimized_field_name='To/Target Class', description='')
    toNam  = StringType(minimized_field_name='To Relationship/Role', description='')
    toGen  = StringType(minimized_field_name='To/Target Gender', description='')
    
    # this rel is a family relationship
    fam    = StringType(minimized_field_name='Family Parternam/Maternal?', description='p=Parternal/m=Maternal type relationship')
    
    mask   = StringType(minimized_field_name='Mask', description='ie. 1, 11')
    
    weight = StringType(minimized_field_name='Sort weight value', description='')

class Dx(_Model):
    '''Used to link two Models/Docs together along with details related describing the relationship.

        NOTE: 
            ways to optimize?
            field to index on?
            how to index?
        '''
    frC     = ObjectIdType(ObjectId) # From/Subject Class
    frID    = ObjectIdType(ObjectId) # From/Subject ID

    toC     = ObjectIdType(ObjectId) # To Parent Class
    toID    = ObjectIdType(ObjectId) # Parent ID

    dxRelID = ObjectIdType(ObjectId) # DxRel ID
    
    # created
    cBy      = ObjectIdType(ObjectId)
    mOn      = DateTimeType()
    cPl      = StringType(minimized_field_name='Place', description='')
    
    # modified
    mBy      = ObjectIdType(ObjectId)
    mOn      = DateTimeType()
    mPl      = StringType(minimized_field_name='Place', description='')
    
    # deleted
    dele     = BooleanType(minimized_field_name='Deleted', description='Marked for removal.')
    
    
    relTitle = StringType(minimized_field_name='Role/relationship/title')
    relDesc  = StringType(minimized_field_name='Role/relationship description, ie, Job Description.')
    weight   = FloatType(minimized_field_name='Sort weight', description='Sort list by weight value.')
    note     = StringType(minimized_field_name='Note', description='More relation/role details.')

class Cnt(Mod):

    # these may be put into base model Mod

    '''To/Parent/Target relationship details which are embedded into a ListType named tos.
        This is one element in an array/List of ToRels all the way to the root/top item in path.
        First element will be the root/top item/obj in path.
        NOTE:
            Accomodate access/visibility controls? If target (rel)ationship is not viewable based on share options, then user should not see this relationship in list. Right?
        ''' 


    # tos: ie, parents
    tos = ListType(ModelType(Rel))

    # frs: froms, ie, children
    frs = ListType(ModelType(Rel))

    shares    = ListType(ModelType(Share), minimized_field_name='Share List', description='List of Share docs that describe who and at what level/role this doc is shared with.')

    meta   = {
        'collection': 'contacts',
        '_c': 'cnt',
        }
