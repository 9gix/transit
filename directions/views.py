from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.conf import settings
from geopy import geocoders
from directions.forms import DirectionForm
from directions.models import Bus, Stop
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from django.contrib import messages

bound = "1.170649,103.556442|1.485734,104.094086"
geocoder = geocoders.GoogleV3()

distance = D(km=1)

class FindBusView(View):
    def get(self, request, *args, **kwargs):
        params = request.GET
        d_from = params.get('from_lat_lng')
        d_to = params.get('to_lat_lng')
#        loc_from = Point(geo_from[1][1], geo_from[1][0])
#        from_buses = Stop.objects.filter(location__distance_lte=(loc_from, distance)).values_list('bus', flat=True).distinct()
        data = {}
        return HttpReponse(data)

class DirectionView(TemplateView):
    template_name = 'directions/index.html'
    def get_context_data(self, **kwargs):
        context = super(DirectionView, self).get_context_data(**kwargs)
        request = self.request
        params = request.GET
        buses = Bus.objects.none()
        if params.get('go') == 'Find Bus':

            d_from = params.get('direction_from')
            d_to = params.get('direction_to')
            q = Q()
            try:
                geo_from = geocoder.geocode(d_from, bounds=bound)
            except ValueError:
                messages.add_message(request, messages.ERROR, "%s not found" %d_from)
            else:
                context['from'] = geo_from[0]
                loc_from = Point(geo_from[1][1], geo_from[1][0])
                from_buses = Stop.objects.filter(location__distance_lte=(loc_from, distance)).values_list('bus', flat=True).distinct()

            try:
                geo_to = geocoder.geocode(d_to, bounds=bound)
            except ValueError:
                messages.add_message(request, messages.ERROR, "%s not found" %d_to)
            else:
                context['to'] = geo_to[0]
                loc_to = Point(geo_to[1][1], geo_to[1][0])
                to_buses = Stop.objects.filter(location__distance_lte=(loc_to, distance)).values_list('bus', flat=True).distinct()

            try:
                buses = set(from_buses) & set(to_buses)
            except UnboundLocalError:
                buses = Bus.objects.none()
            else:
                buses = Bus.objects.filter(id__in=buses)
            finally:
                context['buses'] = buses
        context['form'] = DirectionForm()
        return context
