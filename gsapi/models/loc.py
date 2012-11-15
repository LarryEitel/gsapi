from schematics.types import StringType
from mod import Mod

class Loc(Mod):
    _id  = StringType() # en_US.UTF, etc
    # use base dNam and dNamS for local name

    meta = {
        'collection': 'locs',
        '_c': 'Loc',
        }