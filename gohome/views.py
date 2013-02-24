from django.views.generic import TemplateView
from transit.models import Bus
from transit.utils import geocoding

def find_bus_nearby(location, nearby_distance=0.1):
    pass

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.GET:
            location1, location2 = self.request.GET['from'], self.request.GET['to']
            a = geocoding(location1)
            b = geocoding(location2)
            buses_A = find_bus_nearby(a)
            buses_B = find_bus_nearby(b)

            buses = list(set(buses_A) & set(buses_B))
            context['buses'] = buses

        context['buses'] = Bus.all()
        return context
    template_name = 'home.html'
