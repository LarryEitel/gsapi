# from . import generic, contact
import models

_cs = {
    'Cnt': {'coll': 'cnts', 'modelClass': getattr(models, 'Cnt')},
    'Cmp': {'coll': 'cnts', 'modelClass': getattr(models, 'Cmp')},
    'Prs': {'coll': 'cnts', 'modelClass': getattr(models, 'Prs')},
    'Usr': {'coll': 'cnts', 'modelClass': getattr(models, 'Usr')},
    'Email': {'modelClass': getattr(models, 'Email')},
    }