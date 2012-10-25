from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Phone, Im
from place import PlaceRel

class DocRel():
    # document model class
    # this is actually embedded in docID but in this context, will be convenient 
    docC         = ObjectIdType(ObjectId)
    docID        = ObjectIdType(ObjectId)
    relDNam      = StringType(minimized_field_name="Relation/Role")
    relDNamShort = StringType(minimized_field_name="Relation/Role Short")
    docDNam      = StringType(minimized_field_name="Doc Display Name")
    docDNamShort      = StringType(minimized_field_name="Doc Display Name Short")

class Rel(_Model):
    # Parent OID of DocX
    parID       = ObjectIdType(ObjectId)

    # array of all ancestors
    # Note: each element needs to persist Cnt.OID, dNam
    # that way UI can display each element of ancestors with links
    # this way no need to also show dNam, dNamShort for this aPath
    docRels = ListType(ObjectIdType(DocRel))
    
    # in a list of aPath's, sort list on this value to control order
    weight    = StringType(minimized_field_name='Sort weight value', description='')


class DocXRel(Mod):
    '''Specifies the relationship between document objects. '''
    fromC    = StringType(minimized_field_name='From/Subject Class', description='')
    toC      = StringType(minimized_field_name='To/Target Class', description='')
    fromGen  = StringType(minimized_field_name='From/Subject Gender', description='')
    fromGen  = StringType(minimized_field_name='From/Subject Gender', description='')
    toGen    = StringType(minimized_field_name='To/Target Gender', description='')
    fam   = StringType(minimized_field_name='Family Parternam/Maternal?', description='p=Parternal/m=Maternal type relationship')
    toName   = StringType(minimized_field_name='To Relationship/Role', description='')
    fromName = StringType(minimized_field_name='From Relationship/Role', description='')
    weight   = StringType(minimized_field_name='Sort weight value', description='')
    mask     = StringType(minimized_field_name='Mask', description='ie. 1, 11')

class DocX(_Model):
    _id      = doc_c + doc_id
    parID    = ObjectIdType(ObjectId) # Parent OID of DocX
    relID    = ObjectIdType(ObjectId) # OID of DocXRel
    
    # created
    cBy      = ObjectIdType(ObjectId)
    cOn      = DateTimeType()
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
    where    = StringType(minimized_field_name='Where', description='More location details.')

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

    # relationships/roles
    rels = ListType(ModelType(Rel))

    notes       = ListType(ModelType(Note), minimized_field_name='Notes', description='')

    meta   = {
        'collection': 'contacts',
        '_c': 'cnt',
        }
