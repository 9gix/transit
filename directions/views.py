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
from django.conf import settings
from urlparse import urlparse, urljoin, urlunparse, parse_qs

from urllib import unquote, urlencode
import urllib2
from lxml import etree
from datetime import datetime
from django.utils.dateparse import parse_datetime
import pytz


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

class MytransportDataset(object):
    skip_interval = 50
    skip = 0
    key = settings.MYTRANSPORT_ACCOUNT_KEY
    guid = settings.MYTRANSPORT_GUID
    base_url = urlparse("http://datamall.mytransport.sg/ltaodataservice.svc/")

    def __init__(self):
        pass

    def get_dataset_url(self, dataset):
        return urljoin(self.base_url.geturl(), dataset)


    def get_query(self):
        return {}

    def get_url(self, dataset):
        url_parts = list(self.base_url)
        url_parts[2] = urljoin(url_parts[2], dataset)
        url_parts[4] = unquote(urlencode(self.get_query()))
        url = urlunparse(url_parts)
        return url

    def fetch(self):
        opener = urllib2.build_opener()
        opener.addheaders = [
            ('AccountKey', self.key),
            ('UniqueUserID', self.guid)]
        for dataset in self.get_dataset_list():
            while (True):
                data_list = self.process(dataset, opener)
                if data_list:
                    self.save(data_list)
                    self.skip += self.skip_interval
                else:
                    break
                print self.skip

    def process(self, dataset, opener):
        url = self.get_url(dataset)
        result = opener.open(url)
        content = result.read()
        data_list = self.process_data(content)
        return data_list


    def get_dataset_list(self):
        raise NotImplementedError

    def process_result(self, result):
        raise NotImplementedError

class MytransportBusStopDataset(MytransportDataset):
    def get_query(self):
        return {
            '$skip':self.skip,
        }

    def get_dataset_list(self):
        return ['BusStopCodeSet']

    def process_data(self, data):
        stop_list = []
        feed = etree.fromstring(data)
        nsmap = feed.nsmap
        nsmap['atom'] = nsmap[None]
        entries = feed.findall('atom:entry', nsmap)
        for entry in entries:
            content = entry.find('atom:content', nsmap)
            properties = content.find('m:properties', nsmap)

            # Properties
            bscode_id = properties.find('d:BusStopCodeID', nsmap).text
            code = properties.find('d:Code', nsmap).text
            road = properties.find('d:Road', nsmap).text
            description = properties.find('d:Description', nsmap).text
            layout_num = properties.find('d:Layout_Num', nsmap).text
            #max_pages = properties.find('d:MaxPages', nsmap).text
            created_at = properties.find('d:CreateDate', nsmap).text
            stop_list.append({
                'bus_stop_code_id': bscode_id,
                'code': code,
                'road': road,
                'description': description,
                'layout_num': layout_num,
            #    'max_pages': max_pages,
                'created_at': created_at,
            })
        return stop_list

    def save(self, data_list):
        for data in data_list:
            created_at = parse_datetime(data['created_at'])
            created_at = pytz.timezone(settings.TIME_ZONE).localize(created_at)

            print 'Saving %s' %data['code']
            stop, created = Stop.objects.get_or_create(code=data['code'],
                    defaults={
                        'road': data['road'],
                        'description': data['description'],
                        'created_at': created_at,
                    })
            if not created:
                stop.road = data['road']
                stop.description = data['description']
                stop.created_at = created_at
                stop.save()


class MytransportBusServiceDataset(MytransportDataset):
    def get_dataset_list(self):
        return ['SMRTInfoSet', 'SBSTInfoSet']

    def process_data(self, data):
        pass

class MytransportBusRouteDataset(MytransportDataset):
    def get_dataset_list(self):
        return ['SMRTRouteSet', 'SBSTRouteSet']

    def process_data(self, data):
        pass
