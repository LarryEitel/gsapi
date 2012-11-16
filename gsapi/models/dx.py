from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Note
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
    dId    = ObjectIdType(ObjectId)
    
    # doc Class
    # ie, pl for Place
    d_c    = ObjectIdType(ObjectId)
    
    # doc Relation Display Name 
    # ie, Administrator
    dxNam  = StringType(minimized_field_name="Relation/Role")
    
    # doc Relation Display Name Short
    # ie, admin
    dxNamS = StringType(minimized_field_name="Relation/Role Short")
    
    ddNam  = StringType(minimized_field_name="Doc Display Name")
    ddNamS = StringType(minimized_field_name="Doc Display Name Short")

class DRel(_Model):
    '''Doc Relationship 
    # In a list of (rel)ationships, ie, Companies (cmp), Persons (prs), Places (pl), Events (ev), etc, docC = the class so that client can retrieve place (rel)ationships for example.
       '''
    # QUESTION: needed? In an embedded list of DRel, and wanna update a specific one, this can be the key for the list
    dxId      = ObjectIdType(ObjectId)

    # Doc Class is the doc Class of the immediate parent/to OR child/fr/from in the array/list of IDs/dRels
    d_c       = StringType(minimized_field_name='Document class', description="doc class of immediate parent/to OR child/fr")
    
    dRelTitle = StringType(minimized_field_name='Role/relationship/title')
    dRelDesc  = StringType(minimized_field_name='Role/relationship description, ie, Job Description.')
    
    # List of Doc IDs in the relToFms list. This is used to quickly check whether a doc ID is referenced.
    # This should be reviewed for effeciency
    ids       = ListType(ObjectIdType(ObjectId))
    
    # List of (rel)ationship details
    dRelToFrs = ListType(ModelType(DRelToFr))
    
    # in a list of aPath's, sort list on this value to control order
    w         = FloatType(minimized_field_name='Sort weight value', description='')
    
    note      = ModelType(Note)

class DxRel(Mod):
    '''Collection of relationship description/titles between document objects. '''
    fr_c   = ListType(StringType())
    frNam  = StringType(minimized_field_name='From Relationship/Role', description='')
    frNamS = StringType(minimized_field_name='From Relationship/Role', description='')
    frGen  = StringType(minimized_field_name='From/Subject Gender', description='')
    
    to_c   = ListType(StringType())
    toNam  = StringType(minimized_field_name='To Relationship/Role', description='')
    toNamS = StringType(minimized_field_name='To Relationship/Role', description='')
    toGen  = StringType(minimized_field_name='To/Target Gender', description='')
    
    # this rel is a family relationship
    fam    = StringType(minimized_field_name='Family Parternam/Maternal?', description='p=Parternal/m=Maternal type relationship')
    
    mask   = StringType(minimized_field_name='Mask', description='ie. 1, 11')
    
    w      = FloatType(minimized_field_name='Sort weight value', description='')

class Dx(Mod):
    '''Used to link two Models/Docs together along with reference to rel(ationship) description.
        '''
    fr_c    = ObjectIdType(ObjectId) # From/Subject Class
    frId    = ObjectIdType(ObjectId) # From/Subject ID
    
    to_c    = ObjectIdType(ObjectId) # To Parent Class
    toId    = ObjectIdType(ObjectId) # Parent ID
    
    dxRelId = ObjectIdType(ObjectId) # DxRel ID
    
    meta      = {
        'collection': 'dxs',
        '_c': 'Dx',
        }

