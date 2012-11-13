from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, GeoPointType, URLType, BooleanType, DictType
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Im, Review
from mixins import DxMixin
from schematics.types.mongo import ObjectIdType
from bson import ObjectId

class TagTyp(Mod):
    # model classes that this tag type is relavent 
    mod_cls = ListType(StringType(minimized_field_name='Tag model classes'))
    dNam    = StringType(minimized_field_name='Tag type name')
    dNamS   = StringType(minimized_field_name='Tag type name verbose')
    
    meta    = {
        'collection': 'tagtyps',
        '_c': 'TagTyp',
        }

class Tag(Mod):
    tagTyp    = ListType(ModelType(TagTyp))
    
    nam    = StringType(minimized_field_name='Tag name')
    namS   = StringType(minimized_field_name='Tag name verbose')

    meta       = {
        'collection': 'tags',
        '_c': 'Tag',
        }
