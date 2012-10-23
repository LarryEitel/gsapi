from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, BooleanType
from schematics.types.mongo import ObjectIdType
from bson import ObjectId
import datetime

class Mod(_Model):
    _c   = StringType(required=True, description='Class')
    _public_fields = ['_c']
    # owned
    oBy     = ObjectIdType(ObjectId)
    oOn     = DateTimeType()
    oLoc    = StringType()
    #oPlace    = StringType()

    # created
    cBy     = ObjectIdType(ObjectId)
    cOn     = DateTimeType()
    cLoc    = StringType()
    #cPlace    = StringType()

    # modified
    mBy     = ObjectIdType(ObjectId)
    mOn     = DateTimeType()
    mLoc    = StringType()
    #mPlace    = StringType()

    # deleted
    dele    = BooleanType(minimized_field_name='Deleted', description='Marked for removal.')
    dBy     = ObjectIdType(ObjectId)
    dOn     = DateTimeType()
    dLoc    = StringType()
    #dPlace    = StringType()
    
    note    = StringType()

    meta = {
        '_c': 'mod',
        }

    @property
    def index(self):
        return {}

    @classmethod
    def logit(self, user_id, method='post'):

        # Log this
        now = datetime.datetime.utcnow()

        if method == 'post':
            self.oBy = user_id
            self.oOn = now
            self.cBy = user_id
            self.cOn = now

        self.mBy = user_id
        self.mOn = now

