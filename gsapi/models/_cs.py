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

# let's get the model class for each
_cs_keys = _cs.keys()
for i in range(0, len(_cs)):
	key = _cs_keys[i]
	_cs[key]['modelClass'] = getattr(models, key)