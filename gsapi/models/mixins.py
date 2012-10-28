from schematics.models import Model, Mixin
from schematics.types import (BaseType, StringType, BooleanType, URLType, EmailType, LongType)

# mixins
# https://github.com/j2labs/schematics/blob/master/demos/mixins.py


# create
# RatingType() # https://developers.google.com/gdata/docs/2.0/elements#gdRating


# ResourceType() # https://developers.google.com/gdata/docs/2.0/elements#gdResourceId

class DxMixin(Mixin):
    liked    = BooleanType(default=False)
    rating   = IntType()

    shrs    = ListType(ModelType(Shr), minimized_field_name='Share List', description='List of Share docs that describe who and at what level/role this doc is shared with.')

    # tos: ie, parents
    tos = ListType(ModelType(DRel))

    # frs: froms, ie, children
    frs = ListType(ModelType(DRel))
