from schematics.models import Model as _Model
from schematics.types import StringType

class Id(_Model):
    _c  = StringType()
    id  = LongType()

    meta = {
        'collection': 'ids',
        '_c': 'Id',
        }