from schematics.models import Model as _Model
from schematics.types import StringType

class Slug(_Model):
    _c  = StringType()
    nam  = StringType()
    incr  = IntType()

    meta = {
        'collection': 'slugs',
        '_c': 'Slug',
        }