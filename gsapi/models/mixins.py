from schematics.models import Model, Mixin
from schematics.types import (BaseType, StringType, BooleanType, URLType, EmailType, LongType)
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Phone, Im, Review
from rdt import Rdt

# mixins
# https://github.com/j2labs/schematics/blob/master/demos/mixins.py


# create
# RatingType() # https://developers.google.com/gdata/docs/2.0/elements#gdRating


# ResourceType() # https://developers.google.com/gdata/docs/2.0/elements#gdResourceId

class DxMixin(Mixin):
    typ       = StringType(minimized_field_name='Type of doc.')
    icon      = StringType(minimized_field_name='Place Icon', description='URL to an image resource that can be used to represent this Place\'s type.')
    liked     = BooleanType(default=False)
    # create RatingType
    # https   ://developers.google.com/gdata/docs/2.0/elements#gdRating
    rating    = IntType()
    followers = ListType()
    favorited = IntType()
    
    reviews   = ListType(ModelType(Review))
    
    # long_name
    nam       = StringType(minimized_field_name='Name')
    #short_name
    namS      = StringType(minimized_field_name='NameShort')
    namAlt    = StringType(minimized_field_name='Alternate/informal/colloquial name')
    
    tags      = ListType(StringType(minimized_field_name='Tags', description='General tags.'))
    
    phones    = ListType(ModelType(Phone), minimized_field_name='Phones', description='')
    emails    = ListType(ModelType(Email), minimized_field_name='Emails', description='')
    ims       = ListType(ModelType(Im), minimized_field_name='Instant Message Network', description='')
    
    urls      = ListType(URLType(), minimized_field_name='Urls', description='Urls associated with this doc.')
    rdts      = ListType(ModelType(Rdt))
    notes     = ListType(ModelType(Note))
    
    shrs      = ListType(ModelType(Shr), minimized_field_name='Share List', description='List of Share docs that describe who and at what level/role this doc is shared with.')
    
    # tos     : ie, parents
    tos       = ListType(ModelType(DRel))
    
    # frs     : froms, ie, children
    frs       = ListType(ModelType(DRel))
