from mod import Mod
from schematics.models import Model as _Model
from schematics.types import StringType, FloatType
from schematics.types.compound import ListType, ModelType
from bson import ObjectId

class TagGrp(Mod):
    # model classes that this tag type is relavent 
    # famTags  
    # hobbyTags
    # skillTags
    # bio      
    # pets     
    mod_c   = ListType(StringType(description='Tag model classes'))
    # use base dNam and dNamS for name of tag
    # dNam    = StringType(description='Tag type name')
    # dNamS   = StringType(description='Tag type name verbose')
    
    # in a list of aPath's, sort list on this value to control order
    w       = FloatType(description='Sort weight value')

    meta    = {
        'collection': 'tagtyps',
        '_c': 'TagTyp',
        }

class Tag(Mod):
    tagGrp = ModelType(TagGrp)
    
    # use base dNam and dNamS for name of tag
    # nam    = StringType(description='Tag name')
    # namS   = StringType(description='Tag name verbose')
    
    meta   = {
        'collection': 'tags',
        '_c': 'Tag',
        }
