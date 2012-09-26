from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType
from schematics.types.mongo import ObjectIdType
import datetime

from db import db

class Mod(_Model):
    _c   = StringType(required=True, description='Class')
    _public_fields = ['_c']
    oBy     = ObjectIdType()
    oOn     = DateTimeType() # ObjectIdType()
    oLoc    = StringType()
    cOn     = DateTimeType()
    cBy     = ObjectIdType()
    cLoc    = StringType()
    mOn     = DateTimeType()
    mBy     = ObjectIdType()
    mLoc    = StringType()
    dBy     = ObjectIdType()
    dOn     = DateTimeType()
    dLoc    = StringType()
    note    = StringType()

    meta = {
        'collection': 'contacts',
        '_c': 'Mod',
        }

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

