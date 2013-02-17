from django.conf.urls import patterns, include, url
from django.contrib import admin
from transit.views import FetchBusRouteView, FetchBusServiceView

admin.autodiscover()

urlpatterns = patterns('transit.views',
    url(r'^fetch/(?P<bus_no>\w+)/(?P<bus_route>\w+)/$', FetchBusRouteView.as_view()),
    url(r'^fetch/$', FetchBusServiceView.as_view()),
)
