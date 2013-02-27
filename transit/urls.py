from django.conf.urls import patterns, include, url
from django.contrib import admin
from transit.views import FetchBusStopView, BusStopFetcher, Fetcher

admin.autodiscover()

urlpatterns = patterns('transit.views',
    url(r'^fetch/bus-stop/(?P<zone_segment>\d+)/$', FetchBusStopView.as_view()),
    url(r'^fetcher/bus-stop/', BusStopFetcher.as_view()),
    url(r'^fetch/$', Fetcher.as_view()),
)
