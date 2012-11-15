from schematics.models import Model as _Model
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from loc import Loc

# abbrev country?
class Country(_Model):
    '''
        http://www.iso.org/iso/iso-3166-1_decoding_table
        '''
    _id       = StringType(minimized_field_name='ID', description='Country code as in ISO 3166-1 alpha-2')
    # display
    nam       = StringType(minimized_field_name='Name')
    #short display name
    namS      = StringType(minimized_field_name='NameShort')
    timeZones = ListType(StringType())
    locs      = ListType(ModelType(Loc))

    meta      = {
        'collection': 'countrys',
        '_c': 'Country',
        }
