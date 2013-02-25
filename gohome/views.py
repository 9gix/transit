from django.views.generic import TemplateView
from transit.models import Bus, BusStop
from transit.utils import geocoding, haversine

def find_bus_nearby(location, nearby_distance=0.5):
    busstops = BusStop.all()
    buses = []
    for stop in busstops:
        coord = stop.coordinate
        distance = haversine(coord.lat, coord.lon, location[0], location[1])
        if distance <= nearby_distance:
            for brs in stop.bus_route_stops:
                buses.append(brs.bus_route.bus.no)
    return buses

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.GET:
            location1, location2 = self.request.GET['from'], self.request.GET['to']
            a = geocoding(location1)
            b = geocoding(location2)
            buses_A = find_bus_nearby(a) if a else []
            buses_B = find_bus_nearby(b) if b else []
            buses = list(set(buses_A) & set(buses_B))
            context['from'] = self.request.GET['from']
            context['to'] = self.request.GET['to']
        else:
            buses = []

        context['buses'] = buses
        return context
