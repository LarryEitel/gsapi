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

    dId            = LongType(minimized_field_name='Unique Doc Id')
    collNam        = StringType(minimized_field_name='Collection Name')
    '''Used to tract whether this object was created in base collection or _tmp (temp) collection'''
    isTmp          = LongType(minimized_field_name='Is Temp Doc')
    '''When creating an initialized temp doc, set this flag. It should not be persisted to base collection.'''

    cloned_id      = ObjectIdType(ObjectId)
    '''if this doc has been cloned, set to _id of source doc.'''

    # unique slug value generated on save and optionally used for SEO friendly urls.
    slug           = StringType(minimized_field_name='Unique Slug')

    # display
    dNam           = StringType(minimized_field_name='Name')

    # HTML version of display
    # inspired by value of pre-rendering Pth's in tos/frs
    dNamHTML           = StringType(minimized_field_name='Name')

    #short display name
    # this will default to slug value but can be optionally overwritten
    dNamS          = StringType(minimized_field_name='NameShort')

    locked         = StringType(minimized_field_name='Locked', description='May be set with OID of tmp snapshot of doc being edited.')
    lockedDuration = IntType(minimized_field_name='Lock Duration Time in Minutes', description='')
    '''User will be prompted to continue, save, cancel edit of this doc'''

    publish        = BooleanType(minimized_field_name='Publish', description='')

    dele           = BooleanType(minimized_field_name='Deleted', description='Marked for removal.')
    
    # owned
    oBy            = ObjectIdType(ObjectId)
    oOn            = DateTimeType()
    oPl            = StringType()
    
    # created
    cBy            = ObjectIdType(ObjectId)
    cOn            = DateTimeType()
    cPl            = StringType()
    
    # modified
    mBy            = ObjectIdType(ObjectId)
    mOn            = DateTimeType()
    mPl            = StringType()
    
    # deleted
    dBy            = ObjectIdType(ObjectId)
    dOn            = DateTimeType()
    dPl            = StringType()
    
    
    # note           = ModelType(Note)

    img            = StringType(minimized_field_name='Place Icon', description='URL to an image resource that can be used to represent this object.')
    
    meta           = {
        '_c': 'Mod',
        }

    @property
    def index(self):
        return {}

    @classmethod
    def logit(self, usrId, method='post'):

        # Log this
        now = datetime.datetime.utcnow()

        if method == 'post':
            self.oBy = usrId
            self.oOn = now
            self.cBy = usrId
            self.cOn = now

        self.mBy = usrId
        self.mOn = now

