from math import radians, cos, sin, asin, sqrt, atan2
from urllib import quote_plus
import urllib2
import json
import math
import numpy as np

R = 6371

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth"""
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = R * c
    return km


def geocoding(address):
    address = quote_plus(address)
    url="http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&components=country:SG" % address

    response = urllib2.urlopen(url)
    jsongeocode = json.loads(response.read())
    results = jsongeocode['results']

    if results:
        loc = results[0]['geometry']['location']
        return loc['lat'], loc['lng']
    return None

def dist(p1, p2, p):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p[0], p[1]
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = math.sqrt(dx*dx + dy*dy)

    return dist

def toCartesian(lat, lon):
    """Unsure"""
    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    z = R * sin(lat)
    return x,y,z

def toLatLng(x,y,z):
    """Unsure"""
    lat = asin(z / R)
    lon = atan2(y, x)
    return lat, lon

def nearestPointGreatCircle(a,b,c):
    """Unsure"""
    a = toCartesian(a[0], a[1])
    b = toCartesian(b[0], b[1])
    c = toCartesian(c[0], c[1])
    a1 = np.array(a)
    b1 = np.array(b)
    c1 = np.array(c)

    G = np.cross(a1,b1)
    F = np.cross(c1, G)
    t = np.cross(G, F)

    normalized = t / np.sqrt((t ** 2).sum())
    normalized = R * normalized
    return toLatLng(normalized[0], normalized[1], normalized[2])

