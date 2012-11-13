from schematics.models import Model as _Model
from schematics.types import StringType, DateTimeType, BooleanType
from schematics.types.mongo import ObjectIdType
from bson import ObjectId
import datetime

class Mod(_Model):
    _c             = StringType(required=True, description='Class')
    _public_fields = ['_c']
    
    locked         = BooleanType(minimized_field_name='Locked', description='Marked as locked.')
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
    
    # display
    dNam           = StringType(minimized_field_name='Name')
    #short display name
    dNamS          = StringType(minimized_field_name='NameShort')
    
    icon           = StringType(minimized_field_name='Place Icon', description='URL to an image resource that can be used to represent this Place\'s type.')
    
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

