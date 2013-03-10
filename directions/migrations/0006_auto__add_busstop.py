# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BusStop'
        db.rename_table('directions_bus_stops', 'directions_busstop')


    def backwards(self, orm):
        # Deleting model 'BusStop'
        db.rename_table(u'directions_busstop', 'directions_bus_stops')

    models = {
        u'directions.bus': {
            'Meta': {'object_name': 'Bus'},
            'direction': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directions.Stop']", 'through': u"orm['directions.BusStop']", 'symmetrical': 'False'})
        },
        u'directions.busstop': {
            'Meta': {'object_name': 'BusStop'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Bus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Stop']"})
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
