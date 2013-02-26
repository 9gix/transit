from django.conf.urls import patterns, include, url
from django.contrib import admin
from transit.views import FetchBusRouteView, FetchBusServiceView, \
        FetchBusStopView, BusStopFetcher

admin.autodiscover()

urlpatterns = patterns('transit.views',
    # url(r'^fetch/bus/(?P<bus_no>\w+)/(?P<direction>\w+)/$', FetchBusRouteView.as_view()),
    url(r'^fetch/bus-stop/(?P<zone_segment>\d+)/$', FetchBusStopView.as_view()),
    url(r'^fetcher/bus-stop/', BusStopFetcher.as_view()),
    url(r'^fetch/$', FetchBusServiceView.as_view()),
)
