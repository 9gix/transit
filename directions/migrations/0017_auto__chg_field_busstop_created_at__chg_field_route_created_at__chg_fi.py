# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BusStop.created_at'
        db.alter_column(u'directions_busstop', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Route.created_at'
        db.alter_column(u'directions_route', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Bus.created_at'
        db.alter_column(u'directions_bus', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Stop.created_at'
        db.alter_column(u'directions_stop', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'BusStop.created_at'
        db.alter_column(u'directions_busstop', 'created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 9, 0, 0)))

        # Changing field 'Route.created_at'
        db.alter_column(u'directions_route', 'created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 9, 0, 0)))

        # Changing field 'Bus.created_at'
        db.alter_column(u'directions_bus', 'created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 9, 0, 0)))

        # Changing field 'Stop.created_at'
        db.alter_column(u'directions_stop', 'created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 9, 0, 0)))

    models = {
        u'directions.bus': {
            'Meta': {'object_name': 'Bus'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'directions.busstop': {
            'Meta': {'object_name': 'BusStop'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'distance': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Route']", 'null': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Stop']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'directions.route': {
            'Meta': {'object_name': 'Route'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Bus']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'direction': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True'}),
            'multiline': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directions.Stop']", 'through': u"orm['directions.BusStop']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'directions.stop': {
            'Meta': {'object_name': 'Stop'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'road': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['directions']