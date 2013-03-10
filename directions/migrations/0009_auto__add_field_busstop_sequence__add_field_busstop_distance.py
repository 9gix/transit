# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BusStop.sequence'
        db.add_column(u'directions_busstop', 'sequence',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'BusStop.distance'
        db.add_column(u'directions_busstop', 'distance',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BusStop.sequence'
        db.delete_column(u'directions_busstop', 'sequence')

        # Deleting field 'BusStop.distance'
        db.delete_column(u'directions_busstop', 'distance')


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
            'distance': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Route']", 'null': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Stop']"})
        },
        u'directions.route': {
            'Meta': {'object_name': 'Route'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Bus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'multiline': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directions.Stop']", 'through': u"orm['directions.BusStop']", 'symmetrical': 'False'})
        },
        u'directions.stop': {
            'Meta': {'object_name': 'Stop'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'})
        }
    }

    complete_apps = ['directions']