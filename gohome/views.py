from django.views.generic import TemplateView
from transit.models import Bus, BusStop, Stop
from transit.utils import geocoding, haversine
from math import cos

def find_bus_nearby(location, nearby_distance=1):
    lat, lng = location[0], location[1]
    # Assumption
    # 1 deg Latitude = 111111.1 meter
    # 1 meter = 1 / 111111.1 deg Latitude
    # 1 deg Longitude = 111111.1 * cos(lat) meter
    # 1 meter = 1 / (111111.1 * cos(lat)) deg Longitude
    y_delta = nearby_distance / 111.1111
    x_delta = nearby_distance / (111.1111 * cos(lat))
    north_lat = lat + y_delta # Towards Positive Latitide
    south_lat = lat - y_delta # Towards Negative Latitude
    east_lng = lng + x_delta # Towards Positive Longitude
    west_lng = lng - x_delta # Towards Negative Longitude
    stops_lat_bound = Stop.all(projection=('code',)).filter('lat <=', north_lat).filter('lat >=', south_lat)
    stops_lng_bound = Stop.all(projection=('code',)).filter('lng <=', east_lng).filter('lng >=', west_lng)

    stops_bound = set([stop.code for stop in stops_lat_bound])
    stops_bound.update([stop.code for stop in stops_lng_bound])

    buses = []
    for stop_code in stops_bound:
        stop = Stop.all().filter('code =', stop_code).get()
        distance = haversine(stop.lat, stop.lng, location[0], location[1])
        if distance <= nearby_distance:
            for bus_stop in stop.buses:
                buses.append(bus_stop.bus.no)
    return set(buses)

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        buses = []
        context['bus_exist'] = False
        if self.request.GET:
            location1, location2 = self.request.GET['from'], self.request.GET['to']
            a = geocoding(location1)
            b = geocoding(location2)
            buses_A = find_bus_nearby(a) if a else set()
            buses_B = find_bus_nearby(b) if b else set()

            bus_list = list(buses_A & buses_B)

            buses = Bus.all().filter('no IN', bus_list)
            context['from'] = self.request.GET['from']
            context['to'] = self.request.GET['to']
            context['bus_exist'] = True if buses.get() else False

        context['buses'] = buses

        return context
