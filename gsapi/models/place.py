from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, LongType, StringType, FloatType, DateTimeType, EmailType, GeoPointType, URLType, BooleanType, DictType
from schematics.types.compound import ListType, ModelType
from embed import Email, Note, Phone, Im, Review
from schematics.types.mongo import ObjectIdType
from bson import ObjectId

class Country(_Model):
    '''
        http://www.iso.org/iso/iso-3166-1_decoding_table
        '''
    code      = StringType(minimized_field_name='Code', description='Country code as in ISO 3166-1 alpha-2')
    name      = StringType(minimized_field_name='Name', description='')
    nameLocal = StringType(minimized_field_name='Local Name', description='')

# structuredPostalAddress
# https://developers.google.com/gdata/docs/2.0/elements#gdStructuredPostalAddress
# Postal address split into components. It allows to store the address in locale independent format. The fields can be interpreted and used to generate formatted, locale dependent address. The following elements reperesent parts of the address: agent, house name, street, P.O. box, neighborhood, city, subregion, region, postal code, country. The subregion element is not used for postal addresses, it is provided for extended uses of addresses only. In order to store postal address in an unstructured form formatted address field is provided.

class XGeoPointType(GeoPointType):
    '''Extend schematics GeoPointType to closer emulate Google geoPt
        https://developers.google.com/gdata/docs/2.0/elements#gdGeoPt
        '''
    elev  = FloatType(minimized_field_name='Elevation', description='Elevation in meters. Negative values indicate depths below mean sea level.')
    label = StringType(minimized_field_name='LocalLabel', description='A simple string value used to name this location. It allows UIs to display a label such as "Current Position".')
    #Google time
    now   = DateTimeType(minimized_field_name='Timestamp')

class AddressTypes(_Model):
    addressTypes = {}
    '''
        administrative_area_level_1 = {'us':'Town', 'india':'called something'}
        administrative_area_level_2
        administrative_area_level_3
        agent
        colloquial_area
        country
        floor
        geocode
        intersection
        locality
        natural_feature
        neighborhood
        political
        point_of_interest
        post_box
        postal_code
        postal_code_prefix
        postal_town
        premise
        premise_name
        room
        route
        street_address
        street_number
        sublocality
        sublocality_level_4
        sublocality_level_5
        sublocality_level_3
        sublocality_level_2
        sublocality_level_1
        subpremise
        transit_station
        '''
    def buildPostalAddress():
        pass

class AddressPart(_Model):
    # types come from: AddressTypes.addressTypes
    addressTypes = ListType(StringType(minimized_field_name='Place Type', description='https://developers.google.com/places/documentation/supported_types'))

    # long_name
    name       = StringType(minimized_field_name='Name')

    #short_name
    nameShort  = StringType(minimized_field_name='NameShort')

class PlaceType(_Model):
    '''
        see: https://developers.google.com/places/documentation/supported_types
        accounting
        airport
        amusement_park
        aquarium
        art_gallery
        atm
        bakery
        bank
        bar
        beauty_salon
        bicycle_store
        book_store
        bowling_alley
        bus_station
        cafe
        campground
        car_dealer
        car_rental
        car_repair
        car_wash
        casino
        cemetery
        church
        city_hall
        clothing_store
        convenience_store
        courthouse
        dentist
        department_store
        doctor
        electrician
        electronics_store
        embassy
        establishment
        finance
        fire_station
        florist
        food
        funeral_home
        furniture_store
        gas_station
        general_contractor
        grocery_or_supermarket
        gym
        hair_care
        hardware_store
        health
        hindu_temple
        home_goods_store
        hospital
        insurance_agency
        jewelry_store
        laundry
        lawyer
        library
        liquor_store
        local_government_office
        locksmith
        lodging
        meal_delivery
        meal_takeaway
        mosque
        movie_rental
        movie_theater
        moving_company
        museum
        night_club
        painter
        park
        parking
        pet_store
        pharmacy
        physiotherapist
        place_of_worship
        plumber
        police
        post_office
        real_estate_agency
        restaurant
        roofing_contractor
        rv_park
        school
        shoe_store
        shopping_mall
        spa
        stadium
        storage
        store
        subway_station
        synagogue
        taxi_stand
        train_station
        travel_agency
        university
        veterinary_care
        zoo
        '''
    pass

# make this embedded doc
# not all places have structured address
class PostalAddress(_Model):
    '''https://developers.google.com/gdata/docs/2.0/elements#gdStructuredPostalAddress'''

    address1    = StringType(minimized_field_name='Address1', description="The agent who actually receives the mail. Used in work addresses. Also for 'in care of' or 'c/o'.")
    nameAgent    = StringType(minimized_field_name='Agent', description="The agent who actually receives the mail. Used in work addresses. Also for 'in care of' or 'c/o'.")

    houseName = StringType(minimized_field_name='House Name', description='Used in places where houses or buildings have names (and not necessarily numbers), eg. "The Pillars".')
    street = StringType(minimized_field_name='Street', description='Can be street, avenue, road, etc. This element also includes the house number and room/apartment/flat/floor number.')

    floor = StringType(minimized_field_name='PO Box', description='Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not always mutually exclusive with street.')
    neighborhood = StringType(minimized_field_name='Neighborhood', description='This is used to disambiguate a street address when a city contains more than one street with the same name, or to specify a small place whose mail is routed through a larger postal town. In China it could be a county or a minor city.')
    city = StringType(minimized_field_name='City', description='Can be city, village, town, borough, etc. This is the postal town and not necessarily the place of residence or place of business.')
    subRegion = StringType(minimized_field_name='SubRegion', description='Handles administrative districts such as U.S. or U.K. counties that are not used for mail addressing purposes. Subregion is not intended for delivery addresses.')
    region = StringType(minimized_field_name='Region', description='A state, province, county (in Ireland), Land (in Germany), departement (in France), etc.')

    post_box = StringType(minimized_field_name='PO Box', description='Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not always mutually exclusive with street.')
    postal_code_prefix = StringType(minimized_field_name='Postal Code Prefix', description='Google has it.')
    postal_code = StringType(minimized_field_name='Postal Code', description='Postal code. Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')
    postal_town = StringType(minimized_field_name='Post Town', description='')

    country = StringType(minimized_field_name='Country', description='The name or code of the country.')
    dNam = StringType(minimized_field_name='Display Postal Address', description='The full, unstructured postal address.')


class PlaceRel(Mod):
    '''Specifies the relationship between the containing entity and the contained Place. '''
    name       = StringType(required=True, minimized_field_name='Relationship/Role', description='')
    nameShort  = StringType(minimized_field_name='Relationship/Role Short', description='')
    weight     = StringType(minimized_field_name='Sort weight value', description='')
    place_id   = ObjectIdType()
    meta = {
        '_c': 'placerel',
        }


class Place(Mod):
    '''https://developers.google.com/places/documentation/details
        https://developers.google.com/maps/documentation/javascript/places#place_details_responses
        '''
    addressParts = ListType(ModelType(AddressPart))

    # long_name
    name       = StringType(minimized_field_name='Name')

    #short_name
    nameShort  = StringType(minimized_field_name='NameShort')
    nameAlt    = StringType(minimized_field_name='Alternate/informal/colloquial name')

    tags       = ListType(StringType(minimized_field_name='Tags', description='General tags.'))
    accessTags = ListType(StringType(minimized_field_name='Tags', description='Restricted, intercom, guard, etc'))
    status     = ListType(StringType(minimized_field_name='Status', description='do_not_call, busy, nh, etc'))

    # create RatingType
    # https://developers.google.com/gdata/docs/2.0/elements#gdRating
    rating     = IntType(minimized_field_name='Rating', description='')
    reviews    = ListType(ModelType(Review))

    # types [ "locality", "political" ]
    placeTypes = ListType(StringType(minimized_field_name='Place Type', description='https://developers.google.com/places/documentation/supported_types'))

    mUnit      = BooleanType(default=False, minimized_field_name='Is Multi-Unit premise.')
    mLevel     = BooleanType(default=False, minimized_field_name='Is Multi-Level premise.')

    # put in PostalAddress?
    postalAddress = PostalAddress()

    color1     = StringType(minimized_field_name='Primary Color', description='')
    color2     = StringType(minimized_field_name='Secondary Color', description='')
    desc       = StringType(minimized_field_name='Description', description='')

    postcode     = StringType(minimized_field_name='Postal Code', description='Postal code. Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')
    utcOffset    = LongType(minimized_field_name='Offset from UTC', description='The number of minutes this Place\'s current timezone is offset from UTC. For example, for Places in Sydney, Australia during daylight saving time this would be 660 (+11 hours from UTC), and for Places in California outside of daylight saving time this would be -480 (-8 hours from UTC).')

    # urls         = ListType(ModelType(URLType), minimized_field_name='Urls', description='Urls associated with this place.')
    #imgs         = ListType(ModelType(Img), minimized_field_name='Images', description='Images associated with this place.')
    phones       = ListType(ModelType(Phone), minimized_field_name='Phones', description='Phones associated with this place.')
    emails       = ListType(ModelType(Email), minimized_field_name='Emails', description='Emails associated with this place.')

    icon         = StringType(minimized_field_name='Place Icon', description='URL to an image resource that can be used to represent this Place\'s type.')

    postcode     = StringType(minimized_field_name='Postal Code', description='Postal code. Usually country-wide, but sometimes specific to the city (e.g. "2" in "Dublin 2, Ireland" addresses).')

    parent      = ListType(ObjectIdType(ObjectId))
    ancestors   = ListType(ObjectIdType(ObjectId))
    descendants = ListType(ObjectIdType(ObjectId))
    notes       = ListType(ModelType(Note))

    aPath        = StringType(minimized_field_name="Verbose Ancestor Path")
    aPathShort   = StringType(minimized_field_name="Ancestor Path Short")
    dNam         = StringType(minimized_field_name="Display Verbose")
    dNamShort    = StringType(minimized_field_name="Display Short")

    poly         = ListType(GeoPointType()) # array of points/locs # boundary of place if an area is involved
    polyOk       = BooleanType()
    bbox         = DictType() # contain topLat, rightLng, bottomLat, leftLng

    geoPt        = GeoPointType() # LNG,LAT, if this involves a boundary, loc becomes center pt
    geoOk        = BooleanType() # empty = unconfirmed

    meta = {
        '_c': 'place',
        }
