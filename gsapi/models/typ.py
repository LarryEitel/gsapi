from schematics.types.compound import ListType, ModelType

from mod import Mod
from loc import Loc


class Typ(Mod):
    '''Type. Model attributes may represent a type, ie, Company (Cmp) may be of a type "Department", Place (Pl) may be of a type "Country".'''
    # use dNam and dNamS for type name 
    
    locs   = ListType(ModelType(Loc))
    
    meta = {
        'collection': 'typs',
        '_c': 'Typ',
        }
