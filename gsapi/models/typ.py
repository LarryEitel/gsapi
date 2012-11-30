from schematics.types.compound import ListType, ModelType

from mod import Mod
from loc import Loc


class Typ(Mod):
    '''Type. Model attributes may represent a type, ie, Company (Cmp) may be of a type "Department", Place (Pl) may be of a type "Country".'''
    # use dNam and dNamS for type name 
    # _id = <_c>.<typ> # Email.work
    # dNam = 'Working'
    # dNamS = 'working'
    # slug = 'work'
    
    meta = {
        'collection': 'typs',
        '_c': 'Typ',
        }

    def typs(self):
    	return {
	    'Email.typ': {'typs': ['home', 'work']}, 
	    'Tel.typ': {'typs': ['home', 'work']}
	    }

# TODOs:
# * read data/collections/typs.yaml
# * load that data into typs collection
# * read mongo typs collection data into flask.g.typs['_c']
 
# Email.typs = g.typs['Email']
# Email.typs['Work'] = localVersion (default Key)
# Email.typs['Work'] = {'dNam': 'Work', 'dNamS': 'work'}
