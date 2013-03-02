from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from directions.views import DirectionView

urlpatterns = patterns('directions.views',
    url(r'^$', DirectionView.as_view()),
)
