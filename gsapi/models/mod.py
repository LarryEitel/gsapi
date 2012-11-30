from schematics.models import Model as _Model
from schematics.types import StringType, IntType, LongType, DateTimeType, BooleanType
from schematics.types.mongo import ObjectIdType
from schematics.types.compound import ModelType
from bson import ObjectId
# from embed import Note
# from typ import Typ
import datetime

#class ModIndex(_Model):
    #def __init__():
        #"parsedtext": self.gatherKeywords(),
        #"dNam"      : self.dNam,
        #"dNamS"     : self.dNamS,
        #"oOn"       : self.oOn
        
class Mod(_Model):
    _c             = StringType(required=True, description='Class')
    # _c             = StringType(description='Class')
    _public_fields = ['_c']
    
    # optional. A model that exents from Mod may choose to impliment an incremented key value similar to a RDBMS incremented primary key.
    # It is the responsibility of the extended model to manage uniqueness if this field/attribute is used.

    # dId            = LongType(description='Unique Doc Id')
    dId            = LongType(default=0)
    
    isTmp          = BooleanType(description='Is Temp Doc')
    '''When creating an initialized temp doc, set this flag. It should not be persisted to base collection.'''

    # cloned_id      = ObjectIdType(ObjectId)
    '''if this doc has been cloned, set to _id of source doc.'''

    # unique slug value generated on save and optionally used for SEO friendly urls.
    slug           = StringType(description='Unique Slug')

    # display
    dNam           = StringType(description='Name')

    # HTML version of display
    # inspired by value of pre-rendering Pth's in tos/frs
    # dNamHTML           = StringType(description='Name')

    #short display name
    # this will default to slug value but can be optionally overwritten
    dNamS          = StringType(description='NameShort')

    # locked         = StringType(description='Locked, May be set with OID of tmp snapshot of doc being edited.')
    # lockedDuration = IntType(default=0)
    '''Lock Duration Time in Minutes. User will be prompted to continue, save, cancel edit of this doc'''

    # publish        = BooleanType(description='Publish')

    # dele           = BooleanType(description='Deleted, Marked for removal.')
    
    # # owned
    # oBy            = ObjectIdType()
    # oOn            = DateTimeType()
    # oPl            = StringType()
    
    # # created
    # cBy            = ObjectIdType()
    # cOn            = DateTimeType()
    # cPl            = StringType()
    
    # # modified
    # mBy            = ObjectIdType()
    # mOn            = DateTimeType()
    # mPl            = StringType()
    
    # # deleted
    # dBy            = ObjectIdType()
    # dOn            = DateTimeType()
    # dPl            = StringType()
    
    
    # note           = ModelType(Note)

    # img            = StringType(description='Place Icon, URL to an image resource that can be used to represent this object.')
    
    meta           = {
        'collection': 'docs',
        '_c'        : 'Mod',
        }

    @property
    def index(self):
        return {}
