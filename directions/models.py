from django.db import models

class Bus(models.Model):
    no = models.CharField(max_length=5)
    direction = models.IntegerField()
    stops = models.ManyToManyField('Stop')

    class Meta:
        verbose_name_plural = 'buses'

    def __unicode__(self):
        return self.no

class Stop(models.Model):
    code = models.CharField(max_length=10)
    lat = models.FloatField()
    lon = models.FloatField()

    def __unicode__(self):
        return self.code
