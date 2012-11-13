from mod import Mod
from schematics.types import StringType

class Lang(Mod):
    code   = StringType(minimized_field_name='Code', description='Language code')
    nam    = StringType(minimized_field_name='Name', description='')
    namLoc = StringType(minimized_field_name='Local Name', description='')

    meta       = {
        'collection': 'langs',
        '_c': 'Lang',
        }