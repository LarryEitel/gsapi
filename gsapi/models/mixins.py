# from schematics.models import Mixin
from schematics.types import StringType, IntType, LongType, BooleanType, URLType, EmailType
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Tel, Im, Pth, Review, Shr
from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from tag import Tag
from rdt import Rdt

# mixins
# https://github.com/j2labs/schematics/blob/master/demos/mixins.py

# create
# RatingType() # https://developers.google.com/gdata/docs/2.0/elements#gdRating

# ResourceType() # https://developers.google.com/gdata/docs/2.0/elements#gdResourceId

class ModMixin(object):
    count     = LongType()
    
    liked     = ListType(ObjectIdType(ObjectId))
    # create RatingType
    # https   ://developers.google.com/gdata/docs/2.0/elements#gdRating
    rating    = IntType()
    followers = ListType(ObjectIdType(ObjectId))
    favorited = ListType(ObjectIdType(ObjectId))
    
    reviews   = ListType(ModelType(Review))
    
    tags      = ListType(ModelType(Tag))
    
    tels      = ListType(ModelType(Tel), description='Telephones')
    emails    = ListType(ModelType(Email), description='Emails')
    ims       = ListType(ModelType(Im), description='Instant Message Network')
    
    urls      = ListType(URLType(), description='Urls associated with this doc.')
    rdts      = ListType(ModelType(Rdt))
    desc      = StringType(description='Description')
    notes     = ListType(ModelType(Note))
    
    shrs      = ListType(ModelType(Shr), description='Share List of Share docs that describe who and at what level/role this doc is shared with.')
    
    # tos     : ie, parents
    tos       = ListType(ModelType(Pth))
    
    # frs     : froms, ie, children
    frCount   = IntType()
    frs       = ListType(ModelType(Pth))
    # question how to handle cases where number of frs/children exceed max doc size
    # frFs      = ModelType(GridFs)
