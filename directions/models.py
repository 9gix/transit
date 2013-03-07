from django.contrib.gis.db import models

class Bus(models.Model):
    no = models.CharField(max_length=5)
    direction = models.IntegerField() # Obsolete
    stops = models.ManyToManyField('Stop', through="BusStop") # Obsolete

    class Meta:
        verbose_name_plural = 'buses'

    def __unicode__(self):
        return self.no

class Route(models.Model):
    bus = models.ForeignKey('Bus')
    stops = models.ManyToManyField('Stop', through="BusStop")
    multiline = models.MultiLineStringField()
    line = models.LineStringField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.bus.no

class BusStop(models.Model):
    bus = models.ForeignKey('Bus') # Obsolete
    route = models.ForeignKey('Route', null=True)
    stop = models.ForeignKey('Stop')


    def __unicode__(self):
        return 'Bus %s:%s' % (bus.no, stop.code)


class Stop(models.Model):
    code = models.CharField(max_length=10)
    location = models.PointField(srid=4326, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.code)
