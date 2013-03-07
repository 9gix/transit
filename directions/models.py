from django.contrib.gis.db import models

class Bus(models.Model):
    no = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'buses'

    def __unicode__(self):
        return self.no

    @property
    def total_direction(self):
        return self.route_set.count()

class Route(models.Model):
    bus = models.ForeignKey('Bus')
    stops = models.ManyToManyField('Stop', through="BusStop")
    direction = models.IntegerField(null=True)
    multiline = models.MultiLineStringField(null=True)
    line = models.LineStringField(null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.bus.no

class BusStop(models.Model):
    bus = models.ForeignKey('Bus') # Obsolete (Bus will be linked via route)
    route = models.ForeignKey('Route', null=True)
    stop = models.ForeignKey('Stop')

    sequence = models.IntegerField(null=True)
    distance = models.FloatField(null=True)

    def __unicode__(self):
        return 'Bus %s:%s' % (bus.no, stop.code)


class Stop(models.Model):
    code = models.CharField(max_length=10)
    location = models.PointField(srid=4326, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.code)
