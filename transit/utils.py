from math import radians, cos, sin, asin, sqrt
from urllib import quote_plus
import urllib2
import json


def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on the earth"""
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def geocoding(address):
    address = quote_plus(address)
    url="http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % address

    response = urllib2.urlopen(url)
    jsongeocode = json.loads(response.read())
    results = jsongeocode['results']

    if results:
        loc = results[0]['geometry']['location']
        return loc['lat'], loc['lng']
    return None


