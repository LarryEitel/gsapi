from schematics.models import Model, Mixin
from schematics.types import (BaseType, StringType, BooleanType, URLType, EmailType, LongType)

# mixins
# https://github.com/j2labs/schematics/blob/master/demos/mixins.py


# create
# RatingType() # https://developers.google.com/gdata/docs/2.0/elements#gdRating


# ResourceType() # https://developers.google.com/gdata/docs/2.0/elements#gdResourceId


# Google Data namespace element reference
class CommonMixin(Mixin):
    liked    = BooleanType(default=False)
    archived = BooleanType(default=False)
    deleted  = BooleanType(default=False)
    rating   = IntType()
