from django.http import HttpResponse, Http404
from django.views.generic import View
from google.appengine.api import urlfetch
from google.appengine.ext.db import GeoPt
import urllib2
from pykml import parser
from transit.models import Bus, BusRoute
from bs4 import BeautifulSoup

BASE_URL = "http://www.publictransport.sg/"
BUS_ROUTE_API_PATH = BASE_URL + '/kml/busroutes/'
MAP_URL = BASE_URL + "/content/publictransport/en/homepage/map.html"

class FetchBusServiceView(View):

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
            bus_no, bus_route = bus_service.split('_')
            bus = Bus.get_or_insert(bus_no, no=bus_no)
            route = bus_no + '-' + bus_route
            BusRoute.get_or_insert(route, bus=bus.key())

class FetchBusRouteView(View):

    def get(self, request, bus_no, bus_route, *args, **kwargs):
        data = {'bus_no': bus_no, 'bus_route': bus_route}
        KML_FILE = "%(bus_no)s-%(bus_route)s.kml" % data
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
            bus = Bus.get_or_insert(bus_no, no=bus_no)
            bus.put()

            # Store Bus Routes
            route = bus_no + "-" + bus_route
            routes = [GeoPt(*coord.split(',')[::-1]) for coord in coords]
            bus_route = BusRoute.get_or_insert(route, routes=routes)
            bus_route.routes = routes
            bus_route.put()

            return HttpResponse("Ok")
