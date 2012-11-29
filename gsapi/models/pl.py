from mod import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, GeoPointType, URLType, BooleanType, DictType
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Im, Review
from mixins import ModMixin
from loc import Loc
from typ import Typ
from schematics.types.mongo import ObjectIdType
from bson import ObjectId

# structuredPostalAddress
# https://developers.google.com/gdata/docs/2.0/elements#gdStructuredPostalAddress
# Postal address split into components. It allows to store the address in locale independent format. The fields can be interpreted and used to generate formatted, locale dependent address. The following elements reperesent parts of the address: agent, house name, street, P.O. box, neighborhood, city, subregion, region, postal code, country. The subregion element is not used for postal addresses, it is provided for extended uses of addresses only. In order to store postal address in an unstructured form formatted address field is provided.

class GeoPtTyp(GeoPointType):
    '''Extend schematics GeoPointType to closer emulate Google geoPt
        https://developers.google.com/gdata/docs/2.0/elements#gdGeoPt
        '''
    elev = FloatType(description='Elevation in meters. Negative values indicate depths below mean sea level.')

class AddrPart(_Model):
    # description ='Address Type', description='https://developers.google.com/places/documentation/supported_types'
    typ  = ModelType(Typ)
    
    # long_name
    nam  = StringType(description='Name')
    
    #short_name
    namS = StringType(description='NameShort')

# make this embedded doc
# not all places have structured address
class PostalAddr(Mod):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdStructuredPostalAddress'''

    addr1            = StringType(description='Address1')
    addr2            = StringType(description='Address2')
    namAgent         = StringType(description="Agent who actually receives the mail. Used in work addresses. Also for 'in care of' or 'c/o'.")
    
    houseNam         = StringType(description='House Name Used in places where houses or buildings have names (and not necessarily numbers), eg. "The Pillars".')
    street           = StringType(description='Street Can be street, avenue, road, etc. This element also includes the house number and room/apartment/flat/floor number.')
    
    floor            = StringType(description='PO Box Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not always mutually exclusive with street.')
    neighborhood     = StringType(description='Neighborhood This is used to disambiguate a street address when a city contains more than one street with the same name, or to specify a small place whose mail is routed through a larger postal town. In China it could be a county or a minor city.')
    city             = StringType(description='Can be city, village, town, borough, etc. This is the postal town and not necessarily the place of residence or place of business.')
    subRegion        = StringType(description='SubRegion Handles administrative districts such as U.S. or U.K. counties that are not used for mail addressing purposes. Subregion is not intended for delivery addresses.')
    region           = StringType(description='Region A state, province, county (in Ireland), Land (in Germany), departement (in France), etc.')
    
    postBox          = StringType(description='PO Box Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not always mutually exclusive with street.')
    postalCodePrefix = StringType(description='Postal Code Prefix Google has it.')
    postalCode       = StringType(description='Postal Code Postal code. Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')
    postalTown       = StringType(description='Post Town')
    country          = StringType(description='Country')

    meta             = {
        '_c': 'PostalAddr',
        }

class Poly(_Model):
    poly       = ListType(GeoPtTyp()) # array of points/locs # boundary of place if an area is involved
    bBox       = DictType() # contain topLat, rightLng, bottomLat, leftLng
    centerPt   = GeoPointType() # LNG,LAT, if this involves a boundary, loc becomes center pt
    centerPtOk = BooleanType() # empty = unconfirmed

class Pl(Mod, ModMixin):
    '''https://developers.google.com/places/documentation/details
        https://developers.google.com/maps/documentation/javascript/places#place_details_responses
        '''
    
    status     = ListType(StringType(description='Status do_not_call, busy, nh, etc'))
    
    mUnit      = BooleanType(default=False, description='Is Multi-Unit premise.')
    mLevel     = BooleanType(default=False, description='Is Multi-Level premise.')
    
    addrParts  = ListType(ModelType(AddrPart))
    # put in PostalAddress?
    postalAddr = PostalAddr()
    
    color1     = StringType(description='Primary Color')
    color2     = StringType(description='Secondary Color')
    
    utcOffset  = LongType(description='Offset from UTC The number of minutes this Place\'s current timezone is offset from UTC. For example, for Places in Sydney, Australia during daylight saving time this would be 660 (+11 hours from UTC), and for Places in California outside of daylight saving time this would be -480 (-8 hours from UTC).')
    
    # urls     = ListType(ModelType(URLType), description='Urls', description='Urls associated with this place.')
    #imgs      = ListType(ModelType(Img), description='Images', description='Images associated with this place.')
    
    
    postCode   = StringType(description='Postal Code Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')
    
    polys      = ListType(ModelType(Poly)) # array of an array of points/locs
    polysOk    = BooleanType()
    bBox       = DictType() # contain topLat, rightLng, bottomLat, leftLng
    
    centerPt      = GeoPointType() # LNG,LAT, if this involves a boundary, loc becomes center pt
    centerPtOk    = BooleanType() # empty = unconfirmed
    
    @property
    def vCenterPt(self):
        '''calc center point. Where there are multiple polys, use largest poly to calc center, unless user supplies centerPt'''
        centerPt = None
        return centerPt

    @property
    def vBBox(self):
        '''calc bounding box'''
        bBox = None
        return bBox

    @property
    def vPoly(self, incElevation):
        '''option to strip out elevation data'''
        poly = self.poly
        return poly

    @property
    def vPostalAddr(self):
        '''Generate postalAddr'''
        self.addrParts = None
        return postalAddr

    meta       = {
        'collection': 'pls',
        '_c': 'Pl',
        }
