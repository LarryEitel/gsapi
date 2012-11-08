from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, GeoPointType, URLType, BooleanType, DictType
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Phone, Im, Review
from mixins import DxMixin
from schematics.types.mongo import ObjectIdType
from bson import ObjectId

# abbrev country?
class Country(_Model):
    '''
        http://www.iso.org/iso/iso-3166-1_decoding_table
        '''
    code   = StringType(minimized_field_name='Code', description='Country code as in ISO 3166-1 alpha-2')
    nam    = StringType(minimized_field_name='Name', description='')
    namLoc = StringType(minimized_field_name='Local Name', description='')

# structuredPostalAddress
# https://developers.google.com/gdata/docs/2.0/elements#gdStructuredPostalAddress
# Postal address split into components. It allows to store the address in locale independent format. The fields can be interpreted and used to generate formatted, locale dependent address. The following elements reperesent parts of the address: agent, house name, street, P.O. box, neighborhood, city, subregion, region, postal code, country. The subregion element is not used for postal addresses, it is provided for extended uses of addresses only. In order to store postal address in an unstructured form formatted address field is provided.

class XGeoPtTyp(GeoPointType):
    '''Extend schematics GeoPointType to closer emulate Google geoPt
        https://developers.google.com/gdata/docs/2.0/elements#gdGeoPt
        '''
    elev  = FloatType(minimized_field_name='Elevation', description='Elevation in meters. Negative values indicate depths below mean sea level.')
    lbl = StringType(minimized_field_name='LocalLabel', description='A simple string value used to name this location. It allows UIs to display a label such as "Current Position".')
    #Google time
    now   = DateTimeType(minimized_field_name='Timestamp')

class AddrPart(_Model):
    # types come from: AddressTypes.addressTypes
    typ = StringType(minimized_field_name='Address Type', description='https://developers.google.com/places/documentation/supported_types')

    # long_name
    nam       = StringType(minimized_field_name='Name')

    #short_name
    namS  = StringType(minimized_field_name='NameShort')

# make this embedded doc
# not all places have structured address
class PostalAddr(_Model):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdStructuredPostalAddress'''

    addr1    = StringType(minimized_field_name='Address1', description="")
    addr2    = StringType(minimized_field_name='Address2', description="")
    namAgent    = StringType(minimized_field_name='Agent', description="The agent who actually receives the mail. Used in work addresses. Also for 'in care of' or 'c/o'.")

    houseNam = StringType(minimized_field_name='House Name', description='Used in places where houses or buildings have names (and not necessarily numbers), eg. "The Pillars".')
    street = StringType(minimized_field_name='Street', description='Can be street, avenue, road, etc. This element also includes the house number and room/apartment/flat/floor number.')

    floor = StringType(minimized_field_name='PO Box', description='Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not always mutually exclusive with street.')
    neighborhood = StringType(minimized_field_name='Neighborhood', description='This is used to disambiguate a street address when a city contains more than one street with the same name, or to specify a small place whose mail is routed through a larger postal town. In China it could be a county or a minor city.')
    city = StringType(minimized_field_name='City', description='Can be city, village, town, borough, etc. This is the postal town and not necessarily the place of residence or place of business.')
    subRegion = StringType(minimized_field_name='SubRegion', description='Handles administrative districts such as U.S. or U.K. counties that are not used for mail addressing purposes. Subregion is not intended for delivery addresses.')
    region = StringType(minimized_field_name='Region', description='A state, province, county (in Ireland), Land (in Germany), departement (in France), etc.')

    postBox = StringType(minimized_field_name='PO Box', description='Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not always mutually exclusive with street.')
    postalCodePrefix = StringType(minimized_field_name='Postal Code Prefix', description='Google has it.')
    postalCode = StringType(minimized_field_name='Postal Code', description='Postal code. Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')
    postalTown = StringType(minimized_field_name='Post Town', description='')

    country = StringType(minimized_field_name='Country', description='The name or code of the country.')
    dNam = StringType(minimized_field_name='Display Postal Address', description='The full, unstructured postal address.')

class Pl(Mod, DxMixin):
    '''https://developers.google.com/places/documentation/details
        https://developers.google.com/maps/documentation/javascript/places#place_details_responses
        '''
    addrParts = ListType(ModelType(AddrPart))

    accessTags = ListType(StringType(minimized_field_name='Tags', description='Restricted, intercom, guard, etc'))
    status     = ListType(StringType(minimized_field_name='Status', description='do_not_call, busy, nh, etc'))

    # types [ "locality", "political" ]
    plTyps = ListType(StringType(minimized_field_name='Place Type', description='https://developers.google.com/places/documentation/supported_types'))

    mUnit      = BooleanType(default=False, minimized_field_name='Is Multi-Unit premise.')
    mLevel     = BooleanType(default=False, minimized_field_name='Is Multi-Level premise.')

    # put in PostalAddress?
    postalAddr = PostalAddr()

    color1     = StringType(minimized_field_name='Primary Color', description='')
    color2     = StringType(minimized_field_name='Secondary Color', description='')
    desc       = StringType(minimized_field_name='Description', description='')

    utcOffset    = LongType(minimized_field_name='Offset from UTC', description='The number of minutes this Place\'s current timezone is offset from UTC. For example, for Places in Sydney, Australia during daylight saving time this would be 660 (+11 hours from UTC), and for Places in California outside of daylight saving time this would be -480 (-8 hours from UTC).')

    # urls         = ListType(ModelType(URLType), minimized_field_name='Urls', description='Urls associated with this place.')
    #imgs         = ListType(ModelType(Img), minimized_field_name='Images', description='Images associated with this place.')


    postCode     = StringType(minimized_field_name='Postal Code', description='Postal code. Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')

    aPath        = StringType(minimized_field_name="Verbose Ancestor Path")
    aPathS   = StringType(minimized_field_name="Ancestor Path Short")

    poly         = ListType(GeoPointType()) # array of points/locs # boundary of place if an area is involved
    polyOk       = BooleanType()
    bBox         = DictType() # contain topLat, rightLng, bottomLat, leftLng

    geoPt        = GeoPointType() # LNG,LAT, if this involves a boundary, loc becomes center pt
    geoOk        = BooleanType() # empty = unconfirmed

    meta = {
        '_c': 'pl',
        }
