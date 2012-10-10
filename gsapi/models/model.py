from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, BooleanType
from schematics.types.mongo import ObjectIdType
import datetime

class Mod(_Model):
    _c   = StringType(required=True, description='Class')
    _public_fields = ['_c']
    # owned
    oBy     = ObjectIdType()
    oOn     = DateTimeType() # ObjectIdType()
    oLoc    = StringType()
    
    # created
    cOn     = DateTimeType()
    cBy     = ObjectIdType()
    cLoc    = StringType()

    # modified
    mOn     = DateTimeType()
    mBy     = ObjectIdType()
    mLoc    = StringType()

    # deleted
    dele    = BooleanType(minimized_field_name='Deleted', description='Marked for removal.')
    dBy     = ObjectIdType()
    dOn     = DateTimeType()
    dLoc    = StringType()
    
    note    = StringType()

    meta = {
        'collection': 'contacts',
        '_c': 'Mod',
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

