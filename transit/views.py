from django.http import HttpResponse, Http404
from django.views.generic import View
from google.appengine.api import urlfetch
from google.appengine.ext.db import GeoPt
import urllib2
import re
from pykml import parser
from transit.models import Bus, BusRoute, BusStop, BusRouteStop
from bs4 import BeautifulSoup

BASE_URL = "http://www.publictransport.sg/"
BUS_ROUTE_API_PATH = BASE_URL + '/kml/busroutes/'
BUS_STOP_API_PATH = BASE_URL + '/kml/busstops/'
MAP_URL = BASE_URL + "/content/publictransport/en/homepage/map.html"

class FetchBusServiceView(View):
    """Fetching all bus services with its direction
    Bus:
        Bus Service No
    BusRoute:
        Direction
    """

    def get(self, request, *args, **kwargs):
        result = urlfetch.fetch(MAP_URL)
        soup = BeautifulSoup(result.content)
        options = soup.find(id='busservice_option').find_all('option')
        bus_service_list = [str(option.attrs.get('value')) for option in options
                if option.attrs.get('value') != 'default']
        self._store(bus_service_list)
        return HttpResponse('Ok')

    def _store(self, bus_service_list):
        for bus_service in bus_service_list:
            bus_no, direction = bus_service.split('_')
            bus = Bus.get_or_insert(bus_no, no=bus_no)
            route = bus_no + '-' + direction
            direction = int(direction)
            bus_route = BusRoute.get_or_insert(route, bus=bus.key(),
                    direction=direction)
            bus_route.direction = direction
            bus_route.put()

class FetchBusStopView(View):
    """Fetching all bus stops information from a given zone segment
    BusStop:
        Bus Stop Code
        Route Sequence
        Coordinate (Lat, Lng)
    Bus:
        Operator (SBS/SMRT)
        Bus Service No
    BusRoute:
        Direction
    """
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
            placemarks = rt.Document.Placemark
            for placemark in placemarks:
                if placemark.styleUrl.text in ['#busStopIcon', '#busStopMixIcon']:
                    coordinate = placemark.Point.coordinates.text

                    geopt = GeoPt(*coordinate.split(',')[::-1])
                    stop_code = placemark.get('id')

                    bus_stop = BusStop.get_or_insert(stop_code,
                            code=stop_code,
                            coordinate=geopt)
                    bus_stop.coordinate = geopt
                    bus_stop.put()


                    # Parsing and Matching the Description which contain data
                    description = placemark.description.text
                    if description:
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
                                    operator=data['operator'])
                            bus.operator = data['operator']
                            bus.put()

                            route_key = "%(no)s-%(direction)s" % data
                            direction = int(data['direction'])
                            bus_route = BusRoute.get_or_insert(route_key,
                                    bus=bus.key(),
                                    direction=direction)
                            bus_route.direction = direction
                            bus_route.save()

                            bus_route_stop_key = "%(no)s-%(route_seq)s" % data
                            brs = BusRouteStop.get_or_insert(bus_route_stop_key,
                                    bus_route=bus_route,
                                    bus_stop=bus_stop,
                                    stop_sequence=int(data['route_seq']),
                                    is_loop=bool(data['loop']))
                            brs.bus_route = bus_route
                            brs.bus_stop = bus_stop
                            brs.stop_sequence = int(data['route_seq'])
                            brs.is_loop = bool(data['loop'])
                            brs.put()
            return HttpResponse("OK")

class FetchBusRouteView(View):
    """Fetching routes
    BusRoute:
        routes
    """

    def get(self, request, bus_no, direction, *args, **kwargs):
        data = {'bus_no': bus_no, 'direction': direction}
        KML_FILE = "%(bus_no)s-%(direction)s.kml" % data
        url = BUS_ROUTE_API_PATH + KML_FILE
        try:
            result = urllib2.urlopen(url)
        except urllib2.HTTPError:
            raise Http404
        else:
            ps = parser.parse(result)
            rt = ps.getroot()
            coords = rt.Document.Placemark.LineString.coordinates.text.split()

            # Store Bus Service
            Bus.get_or_insert(bus_no, no=bus_no)

            # Store Bus Routes
            route = bus_no + "-" + direction
            routes = [GeoPt(*coord.split(',')[::-1]) for coord in coords]
            bus_route = BusRoute.get_or_insert(route, routes=routes)
            bus_route.routes = routes
            bus_route.put()

            return HttpResponse("Ok")
