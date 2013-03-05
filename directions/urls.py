from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from directions.views import DirectionView, FindBusView

urlpatterns = patterns('directions.views',
    url(r'^find-bus/$', FindBusView.as_view()),
    url(r'^$', DirectionView.as_view()),
)
