from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, GeoPointType, URLType, BooleanType, DictType
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Im, Review
from mixins import DxMixin
from schematics.types.mongo import ObjectIdType
from bson import ObjectId

class TagGrp(Mod):
    # model classes that this tag type is relavent 
    # famTags  
    # hobbyTags
    # skillTags
    # bio      
    # pets     
    mod_c   = ListType(StringType(minimized_field_name='Tag model classes'))
    # use base dNam and dNamS for name of tag
    # dNam    = StringType(minimized_field_name='Tag type name')
    # dNamS   = StringType(minimized_field_name='Tag type name verbose')
    
    # in a list of aPath's, sort list on this value to control order
    w       = FloatType(minimized_field_name='Sort weight value', description='')

    meta    = {
        'collection': 'tagtyps',
        '_c': 'TagTyp',
        }

class Tag(Mod):
    tagGrp = ModelType(TagGrp)
    
    # use base dNam and dNamS for name of tag
    # nam    = StringType(minimized_field_name='Tag name')
    # namS   = StringType(minimized_field_name='Tag name verbose')
    
    meta   = {
        'collection': 'tags',
        '_c': 'Tag',
        }
