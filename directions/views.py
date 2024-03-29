from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.conf import settings
from directions.forms import DirectionForm
from directions.models import Bus, Stop, Route, BusStop
from directions.utils.placegeocode import geocode, UnknownPlaceException
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from urlparse import urlparse, urljoin, urlunparse, parse_qs
from ast import literal_eval
from urllib import unquote, urlencode
import urllib2
from lxml import etree
from datetime import datetime
from django.utils.dateparse import parse_datetime
from directions.utils.distance import haversine
import pytz
import logging

logger = logging.getLogger(__name__)

bound = "1.170649,103.556442|1.485734,104.094086"

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

        direction_from = params.get('from','')
        direction_to = params.get('to','')
        geo_from, geo_to = '',''
        a, b = '', ''

        if direction_from and direction_to:
            try:
                direction_from, geo_from = geocode(direction_from)
                direction_to, geo_to = geocode(direction_to)
            except UnknownPlaceException as e:
                messages.error(request,
                    "Couldn't locate %s, please try with another address or place name nearby instead" % e.message)
            else:
                a = Point(geo_from[::-1])
                b = Point(geo_to[::-1])

        route_list = []

        if a and b:
            # All Stop near A
            stopsA = Stop.objects.filter(location__distance_lte=(a, distance))
            if not stopsA:
                messages.warning(request, "There's No Bus Stop near %s"% direction_from)

            # All Stop near B
            stopsB = Stop.objects.filter(location__distance_lte=(b, distance))
            if not stopsB:
                messages.warning(request, "There's No Bus Stop near %s"% direction_to)

            if stopsA and stopsB:
                # All routes between all stops near A & all stops near B
                routes = Route.objects.filter(
                    stops__in=stopsA).filter(stops__in=stopsB).distinct().select_related('bus')

                # All routes from stops A to B
                for route in routes:

                    # lowest Distance at BusStop B
                    busstopB = route.busstop_set.filter(stop__in=stopsB).order_by('distance')
                    if busstopB[0].distance != 0:
                        busstopB = busstopB[0]
                    else:
                        # But if the distance is 0 it means loop to its own station, so the distance was the highest
                        busstopB = busstopB.order_by('-distance')[0]

                    # highest distance at BusStop A
                    busstopA = route.busstop_set.filter(stop__in=stopsA).order_by('-distance')[0]

                    route.travel_distance = busstopB.distance - busstopA.distance

                    l = busstopA.stop.location.tuple
                    walking_distance_A = haversine(l[0], l[1], a.tuple[0], a.tuple[1])

                    l = busstopB.stop.location.tuple
                    walking_distance_B = haversine(l[0], l[1], b.tuple[0], b.tuple[1])

                    route.walking_distance = round(walking_distance_A + walking_distance_B, 1)

                    if route.travel_distance > 0:
                        route_list.append(route)

                sorted_route_list = sorted(route_list, key=lambda k: k.travel_distance + k.walking_distance)
                context['routes'] = sorted_route_list

                if sorted_route_list:
                    route_count = len(sorted_route_list)
                    messages.success(request, "%s bus Founds from %s to %s" % \
                            (route_count, direction_from, direction_to))
                else:
                    messages.info(request, "Sorry, There's no direct Bus from %s to %s"% (direction_from, direction_to))
        context['geo_from'] = geo_from
        context['geo_to'] = geo_to
        context['from'] = direction_from
        context['to'] = direction_to
        return context

class MytransportDataset(object):
    skip_interval = 50
    skip = 0
    key = settings.MYTRANSPORT_ACCOUNT_KEY
    guid = settings.MYTRANSPORT_GUID
    base_url = urlparse("http://datamall.mytransport.sg/ltaodataservice.svc/")

    def __init__(self):
        self.dataset = None

    def get_dataset_url(self, dataset):
        return urljoin(self.base_url.geturl(), dataset)


    def get_query(self):
        return {
            '$skip':self.skip,
        }

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
        while (1):
            url = self.get_url(self.dataset)
            print 'Fetching %s: %s - %s at %s' % (self.dataset, self.skip,  self.skip + self.skip_interval, url)
            result = opener.open(url)
            data_list = self.process(result)
            if data_list:
                self.save(data_list)
                self.skip += self.skip_interval
            else:
                break

    def process(self, result):
        content = result.read()

        data_list = []
        feed = etree.fromstring(content)
        self.nsmap = feed.nsmap
        self.nsmap['atom'] = self.nsmap[None]
        entries = feed.findall('atom:entry', self.nsmap)
        for entry in entries:
            content = entry.find('atom:content', self.nsmap)
            properties = content.find('m:properties', self.nsmap)
            data_list.append(self.process_properties(properties))
        return data_list


    def get_dataset_list(self):
        raise NotImplementedError

    def process_result(self, result):
        raise NotImplementedError

class MytransportBusStopDataset(MytransportDataset):
    def __init__(self):
        self.dataset = 'BusStopCodeSet'

    def process_properties(self, properties):
        nsmap = self.nsmap
        # Properties
        bscode_id = properties.find('d:BusStopCodeID', nsmap).text
        code = properties.find('d:Code', nsmap).text
        road = properties.find('d:Road', nsmap).text
        description = properties.find('d:Description', nsmap).text
        layout_num = properties.find('d:Layout_Num', nsmap).text
        #max_pages = properties.find('d:MaxPages', nsmap).text
        created_at = properties.find('d:CreateDate', nsmap).text
        created_at = parse_datetime(created_at)
        created_at = pytz.timezone(settings.TIME_ZONE).localize(created_at)
        return {
            'bus_stop_code_id': bscode_id,
            'code': code,
            'road': road,
            'description': description,
            'layout_num': layout_num,
        #    'max_pages': max_pages,
            'created_at': created_at,
        }

    def save(self, data_list):
        for data in data_list:
            print 'Saving %s' %data['code']
            stop, created = Stop.objects.get_or_create(code=data['code'],
                    defaults={
                        'road': data['road'],
                        'description': data['description'],
                        'created_at': data['created_at'],
                    })
            if not created:
                stop.road = data['road']
                stop.description = data['description']
                stop.created_at = data['created_at']
                stop.save()


class MytransportBusRouteDataset(MytransportDataset):
    def process_properties(self, properties):
        nsmap = self.nsmap
        # Properties
        svc_no = properties.find('d:SR_SVC_NUM', nsmap).text
        svc_dir = properties.find('d:SR_SVC_DIR', nsmap).text
        route_seq = properties.find('d:SR_ROUT_SEQ', nsmap).text
        stop_code = properties.find('d:SR_BS_CODE', nsmap).text
        distance = properties.find('d:SR_DISTANCE', nsmap).text
        try:
            distance = float(distance)
        except ValueError:
            distance = 0.0
        created_at = properties.find('d:CreateDate', nsmap).text
        created_at = parse_datetime(created_at)
        created_at = pytz.timezone(settings.TIME_ZONE).localize(created_at)
        return {
            'svc_no': svc_no,
            'svc_dir': svc_dir,
            'route_seq': route_seq,
            'stop_code': stop_code,
            'distance': distance,
            'created_at': created_at,
        }

    def save(self, data_list):
        for data in data_list:
            bus, created = Bus.objects.get_or_create(no=data['svc_no'])
            route, created = Route.objects.get_or_create(bus=bus, direction=data['svc_dir'])
            stop, created = Stop.objects.get_or_create(code=data['stop_code'])

            bus_stop, created = BusStop.objects.get_or_create(route=route, stop=stop, sequence=data['route_seq'],
                    defaults={
                        'distance': data['distance'],
                        'created_at': data['created_at'],
                    })

            if not created:
                bus_stop.distance = data['distance']
                bus_stop.created_at = data['created_at']
                stop.save()

            print "Saved: Bus %s - Stop %s" % (bus.no, stop.code)

class MytransportSMRTBusRouteDataset(MytransportBusRouteDataset):
    def __init__(self):
        self.dataset = 'SMRTRouteSet'

class MytransportSBSTBusRouteDataset(MytransportBusRouteDataset):
    def __init__(self):
        self.dataset = 'SBSTRouteSet'

"""NOT USED"""
class MytransportBusServiceDataset(MytransportDataset):
    pass

class MytransportSMRTBusServiceDataset(MytransportBusServiceDataset):
    def __init__(self):
        self.dataset = 'SMRTInfoSet'

class MytransportSBSTBusServiceDataset(MytransportBusServiceDataset):
    def __init__(self):
        self.dataset = 'SBSTInfoSet' 
