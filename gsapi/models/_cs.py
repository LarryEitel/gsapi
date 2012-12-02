# from . import generic, contact
import models

# _c = Model Class name
# all class names
# collNam = collection name
_cs = {
	'Cmp'    : {'collNam': 'cnts'},
	'Cnt'    : {'collNam': 'cnts'},
	'Country': {'collNam': 'countrys'},
	'Email'  : {},
	'Event'  : {'collNam': 'events'},
	'Im'     : {},
	'Lang'   : {'collNam': 'langs'},
	'Lnk'    : {},
	'Loc'    : {'collNam': 'locs'},
	'Loc'    : {'collNam': 'locs'},
	'Note'   : {},
	'Pl'     : {'collNam': 'pls'},
	'Prs'    : {'collNam': 'cnts'},
	'Pth'    : {},
	'Rdt'    : {},
	'Review' : {},
	'Tag'    : {'collNam': 'tags'},
	'TagGrp' : {'collNam': 'taggrps'},
	'Tel'    : {},
	'Usr'    : {'collNam': 'cnts'},
	'Wdg'    : {'collNam': 'wdgs'},
    }
    
# collection names
colls = {
	'cnts'    : {'_c': 'Cmp'},
	'cnts'    : {'_c': 'Cnt'},
	'countrys': {'_c': 'Country'},
	'events'  : {'_c': 'Event'},
	'langs'   : {'_c': 'Lang'},
	'locs'    : {'_c': 'Loc'},
	'locs'    : {'_c': 'Loc'},
	'pls'     : {'_c': 'Pl'},
	'cnts'    : {'_c': 'Prs'},
	'tags'    : {'_c': 'Tag'},
	'taggrps' : {'_c': 'TagGrp'},
	'cnts'    : {'_c': 'Usr'},
	'wdgs'    : {'_c': 'Wdg'},
    }

# let's get the model class for each
_cs_keys = _cs.keys()
for i in range(0, len(_cs)):
	key = _cs_keys[i]
	_cs[key]['modelClass'] = getattr(models, key)