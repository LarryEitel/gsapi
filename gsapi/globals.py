import models
from utils import myyaml

# let's get the model class for each
def load():
    g = myyaml.pyObj('globals.yaml')
    _cs = g['_cs']
    _cs_keys = _cs.keys()
    for i in range(0, len(_cs)):
        key = _cs_keys[i]
        try:
            _cs[key]['modelClass'] = getattr(models, key)
        except:
            pass
    g['_cs'] = _cs

    return g

