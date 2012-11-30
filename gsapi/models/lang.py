from mod import Mod
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from loc import Loc

class Lang(Mod):
    _id    = StringType(description='ID, Language code ISO')
    jwId   = StringType(description='JW ID, Language code jw.org')

    # use base dNam, etc
    locs      = ListType(ModelType(Loc))

    meta       = {
        'collection': 'langs',
        '_c': 'Lang',
        }
