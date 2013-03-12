import urllib, urllib2
import json
from django.conf import settings

PLACE_AUTOCOMPLETE_API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json?"
PLACE_DETAIL_API_URL = "https://maps.googleapis.com/maps/api/place/details/json?"


class UnknownPlaceException(Exception):
    pass


def fetch_place_predictions(name):
    params = {
        'input': name,
        'sensor': 'false',
        'key': settings.GOOGLE_API_KEY,
        'components': 'country:sg',
    }
    data = urllib.urlencode(params)
    response = urllib2.urlopen(PLACE_AUTOCOMPLETE_API_URL + data)
    return json.load(response)

def get_best_match(predictions):
    best_match = predictions[0]
    reference = best_match['reference']
    description = best_match['description']
    return reference, description

def fetch_place_detail(reference):
    params = {
        'key': settings.GOOGLE_API_KEY,
        'reference': reference,
        'sensor': 'false',
    }
    data = urllib.urlencode(params)
    response = urllib2.urlopen(PLACE_DETAIL_API_URL + data)
    return json.load(response)

def get_place_location(place_detail):
    location = place_detail['result']['geometry']['location']
    return location['lat'], location['lng']

def geocode(place):
    result = fetch_place_predictions(place)
    if not result['predictions']:
        raise UnknownPlaceException(place)
    reference, description = get_best_match(result['predictions'])
    place_detail = fetch_place_detail(reference)
    lat, lng = get_place_location(place_detail)

    #return place_name, coordinate
    return description, (lat, lng)


