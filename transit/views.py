from django.http import HttpResponse, Http404
from django.views.generic import View
from google.appengine.api import urlfetch
from google.appengine.ext.db import GeoPt
from google.appengine.api import taskqueue
import urllib2
import re
from pykml import parser
from transit.models import Bus, BusStop, Stop
from bs4 import BeautifulSoup
from random import shuffle, randint

BASE_URL = "http://www.publictransport.sg"
BUS_ROUTE_API_PATH = BASE_URL + '/kml/busroutes/'
BUS_STOP_API_PATH = BASE_URL + '/kml/busstops/'
MAP_URL = BASE_URL + "/content/publictransport/en/homepage/map.html"

class FetchBusStopView(View):
    """Fetching all bus stops information from a given zone segment"""

    def get(self, request, zone_segment, *args, **kwargs):
        KML_FILE = "busstops-kml-%s.kml" % zone_segment
        url = BUS_STOP_API_PATH + KML_FILE
        try:
            result = urllib2.urlopen(url)
        except urllib2.HTTPError:
            raise Http404
        else:
            ps = parser.parse(result)
            rt = ps.getroot()
            try:
                placemarks = rt.Document.Placemark
            except AttributeError:
                placemarks = []
            busStyleClasses = ['#busStopIcon', '#busStopMixIcon',
                    '#busStopMixWArrivalIcon', '#busStopWArrivalIcon']
            for placemark in placemarks:
                description = placemark.description.text
                if description and placemark.styleUrl.text in busStyleClasses:
                    coordinate = placemark.Point.coordinates.text

                    lat, lng = [float(coord) for coord in coordinate.split(',')[::-1]]
                    stop_code = placemark.get('id')

                    stop = Stop.get_or_insert(stop_code,
                            code=stop_code,
                            lat=lat,
                            lng=lng)

                    # Parsing and Matching the Description which contain data
                    soup = BeautifulSoup(description)
                    bus_tags = soup.findAll(href=re.compile('doViewBusIndex'))
                    for bus_tag in bus_tags:
                        href = bus_tag['href']
                        regex = re.compile("""
                            '(?P<no>\w+)',
                            '(?P<direction>\d+)',
                            '(?P<route_seq>\d+)',
                            '(?P<bus_stop_code>\d+)',
                            '(?P<operator>\w+)',
                            (?P<loop>\w+)""", re.VERBOSE)
                        match = regex.search(href)

                        data = match.groupdict()
                        bus = Bus.get_or_insert(data['no'],
                                no=data['no'],
                                operator=data['operator'],
                                direction=int(data['direction']))

                        bus_stop_key = "%(bus_stop_code)s-%(no)s" % data
                        bus_stop = BusStop.get_or_insert(bus_stop_key,
                                bus=bus,
                                stop=stop)

            return HttpResponse("OK")

class BusStopFetcher(View):
    def get(self, *args, **kwargs):
        zone_segments = range(1023)
        shuffle(zone_segments)
        for i, zone_segment in enumerate(zone_segments):
            taskqueue.add(
                url='/transit/fetch/bus-stop/%s/' % zone_segment,
                method='GET',
                queue_name='bus-stop-fetcher',
                countdown=i * 60 + randint(1, 1500), # fires about 1 hour each
            )
        return HttpResponse("OK")

class Fetcher(View):
    def get(self, *args, **kwargs):
        taskqueue.add(
            url='/transit/fetcher/bus-stop/',
            method='GET',
        )
        return HttpResponse("Adding Task In Progress")

