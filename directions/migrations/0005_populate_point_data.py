# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.gis.geos import Point

class Migration(DataMigration):

    def forwards(self, orm):
        for stop in orm['directions.Stop'].objects.all():
            stop.location = Point(stop.lon, stop.lat)
            stop.save()


    def backwards(self, orm):
        pass


    models = {
        u'directions.bus': {
            'Meta': {'object_name': 'Bus'},
            'direction': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directions.Stop']", 'symmetrical': 'False'})
        },
        u'directions.stop': {
            'Meta': {'object_name': 'Stop'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['directions']
    symmetrical = True
