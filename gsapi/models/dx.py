from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Phone, Im

'''
    QUESTION:
        class.ID is an ObjectID or ID string?
        If ObjectID, foreign refs to OID vs ID 
        If a String, use ID
        Need a squential Unique number
    '''

'''
    All collections/models/documents (d) based on Mod inherit the following properties and methods:
        - create, modify, owned and deleted logged with: datetime (xOn), user (xBy), place (xPl) 
        - can participate in a hierarchy of documents, ie, can be a parent to or have child docs.
            - parents of a doc are represented in an array named 'tos' which contains a list of DRel docs which contains details including each ancestor beginning with its immediate parent. User interface can render each ancestor in a linkable path.
            - children of a doc are represented in an array named 'frs' which contains a list of DRel docs which contains details relating to each child relationship. User interface can render this along with a link to the referenced child.
            - The relationship between two documents can be viewed from parent (to) to child (fr) or child (fr) to parent (to), ie, Father Bill sees in array of frs a dRel containing Father of Sue.
                Sue would see in her 'tos' a dRel containing Daughter of Bill.
        - access can be controlled by attaching Shr(are) docs in an array of Sh(are)s.
        - can be followed
        - can be liked

    '''


class DRelToFr(_Model):
    '''Doc Relation To and From
        To/Parent/Target/From/Child relationship details which are embedded into a ListType named tos and frs.
        ''' 
    # doc ID
    # 
    dId        = ObjectIdType(ObjectId)

    # doc Class
    # ie, pl for Place
    d_c         = ObjectIdType(ObjectId)

    # doc Relation Display Name 
    # ie, Administrator
    dRelDNam      = StringType(minimized_field_name="Relation/Role")

    # doc Relation Display Name Short
    # ie, admin
    dRelDNamS = StringType(minimized_field_name="Relation/Role Short")

    dDNam      = StringType(minimized_field_name="Doc Display Name")
    dDNamS = StringType(minimized_field_name="Doc Display Name Short")

class DRel(_Model):
    '''Doc Relationship 
    # In a list of (rel)ationships, ie, Companies (cmp), Persons (prs), Places (pl), Events (ev), etc, docC = the class so that client can retrieve place (rel)ationships for example.
       '''
    # Doc Class is the doc Class of the immediate parent/to OR child/fr/from in the array/list of IDs/dRels
    d_c = ObjectIdType(ObjectId)
    
    
    dRelTitle = StringType(minimized_field_name='Role/relationship/title')
    dRelDesc  = StringType(minimized_field_name='Role/relationship description, ie, Job Description.')

    # List of Doc IDs in the relToFms list. This is used to quickly check whether a doc ID is referenced.
    # This should be reviewed for effeciency
    ids   = ListType(ObjectIdType(ObjectId))
    
    # List of (rel)ationship details
    dRelToFrs = ListType(ModelType(DRelToFr))
    
    # in a list of aPath's, sort list on this value to control order
    w     = FloatType(minimized_field_name='Sort weight value', description='')


    note      = StringType(minimized_field_name='Note', description='More relation/role details.')

class DxRel(Mod):
    '''Specifies the relationship between document objects. '''
    fr_c  = StringType(minimized_field_name='From/Subject Class', description='')    
    frNam = StringType(minimized_field_name='From Relationship/Role', description='')
    frGen = StringType(minimized_field_name='From/Subject Gender', description='')
    
    to_c  = StringType(minimized_field_name='To/Target Class', description='')
    toNam = StringType(minimized_field_name='To Relationship/Role', description='')
    toGen = StringType(minimized_field_name='To/Target Gender', description='')
    
    # this rel is a family relationship
    fam   = StringType(minimized_field_name='Family Parternam/Maternal?', description='p=Parternal/m=Maternal type relationship')
    
    mask  = StringType(minimized_field_name='Mask', description='ie. 1, 11')
    
    w     = FloatType(minimized_field_name='Sort weight value', description='')

class Dx(_Model):
    '''Used to link two Models/Docs together along with reference to rel(ationship) description.
        '''
    fr_c    = ObjectIdType(ObjectId) # From/Subject Class
    frId    = ObjectIdType(ObjectId) # From/Subject ID
    
    to_c    = ObjectIdType(ObjectId) # To Parent Class
    toId    = ObjectIdType(ObjectId) # Parent ID
    
    dxRelId = ObjectIdType(ObjectId) # DxRel ID
    
    # created
    cBy     = ObjectIdType(ObjectId)
    cOn     = DateTimeType()
    cPl     = StringType(minimized_field_name='Place', description='')
    
    # modified
    mBy     = ObjectIdType(ObjectId)
    mOn     = DateTimeType()
    mPl     = StringType(minimized_field_name='Place', description='')
    
    # deleted
    dele    = BooleanType(minimized_field_name='Deleted', description='Marked for removal.')
    dBy     = ObjectIdType(ObjectId)
    dOn     = DateTimeType()
    dPl     = StringType()
    
    meta      = {


        'collection': 'dxs',
        '_c': 'dx',
        }


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

    shrs    = ListType(ModelType(Shr), minimized_field_name='Share List', description='List of Share docs that describe who and at what level/role this doc is shared with.')

    meta   = {
        'collection': 'cnts',
        '_c': 'cnt',
        }
