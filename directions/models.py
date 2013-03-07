from django.contrib.gis.db import models

class Bus(models.Model):
    no = models.CharField(max_length=5)
    direction = models.IntegerField()
    stops = models.ManyToManyField('Stop', through="BusStop")

    class Meta:
        verbose_name_plural = 'buses'

    def __unicode__(self):
        return self.no

class Stop(models.Model):
    code = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()

    location = models.PointField(srid=4326, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.code)

class BusStop(models.Model):
    bus = models.ForeignKey('Bus')
    stop = models.ForeignKey('Stop')
    def __unicode__(self):
        return 'Bus %s:%s' % (bus.no, stop.code)
