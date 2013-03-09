# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stop.road'
        db.add_column(u'directions_stop', 'road',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True),
                      keep_default=False)

        # Adding field 'Stop.description'
        db.add_column(u'directions_stop', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Stop.created_at'
        db.add_column(u'directions_stop', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 9, 0, 0)),
                      keep_default=False)

        # Adding field 'Stop.updated_at'
        db.add_column(u'directions_stop', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 3, 9, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stop.road'
        db.delete_column(u'directions_stop', 'road')

        # Deleting field 'Stop.description'
        db.delete_column(u'directions_stop', 'description')

        # Deleting field 'Stop.created_at'
        db.delete_column(u'directions_stop', 'created_at')

        # Deleting field 'Stop.updated_at'
        db.delete_column(u'directions_stop', 'updated_at')


    models = {
        u'directions.bus': {
            'Meta': {'object_name': 'Bus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'directions.busstop': {
            'Meta': {'object_name': 'BusStop'},
            'distance': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Route']", 'null': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Stop']"})
        },
        u'directions.route': {
            'Meta': {'object_name': 'Route'},
            'bus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Bus']"}),
            'direction': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True'}),
            'multiline': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directions.Stop']", 'through': u"orm['directions.BusStop']", 'symmetrical': 'False'})
        },
        u'directions.stop': {
            'Meta': {'object_name': 'Stop'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'road': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['directions']