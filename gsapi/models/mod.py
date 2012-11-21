from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, BooleanType
from schematics.types.mongo import ObjectIdType
from schematics.types.compound import ModelType
from bson import ObjectId
from embed import Note
from typ import Typ
import datetime

class ModIndex(_Model):
    def __init__()
        "parsedtext": self.gatherKeywords(),
        "dNam"      : self.dNam,
        "dNamS"     : self.dNamS,
        "oOn"       : self.oOn

class Mod(_Model):
    _c             = StringType(required=True, description='Class')
    _public_fields = ['_c']
    
    # optional. A model that exents from Mod may choose to impliment an incremented key value similar to a RDBMS incremented primary key.
    # It is the responsibility of the extended model to manage uniqueness if this field/attribute is used.

    id             = LongType()
    cloned_id      = ObjectIdType(ObjectId)
    '''if this doc has been cloned, set to _id of source doc.'''

    # unique slug value generated on save and optionally used for SEO friendly urls.
    slug           = StringType(minimized_field_name='Unique Slug')

    # display
    dNam           = StringType(minimized_field_name='Name')

    #short display name
    # this will default to slug value but can be optionally overwritten
    dNamS          = StringType(minimized_field_name='NameShort')

    locked         = BooleanType(minimized_field_name='Locked', description='Marked as locked.')
    lockedDuration = IntType(minimized_field_name='Lock Duration Time in Minutes', description='')
    '''User will be prompted to continue, save, cancel edit of this doc'''

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
    
    
    note           = ModelType(Note)

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

