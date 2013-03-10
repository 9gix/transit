# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Route.direction'
        db.add_column(u'directions_route', 'direction',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


        # Changing field 'Route.line'
        db.alter_column(u'directions_route', 'line', self.gf('django.contrib.gis.db.models.fields.LineStringField')(null=True))

        # Changing field 'Route.multiline'
        db.alter_column(u'directions_route', 'multiline', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Route.direction'
        db.delete_column(u'directions_route', 'direction')


        # Changing field 'Route.line'
        db.alter_column(u'directions_route', 'line', self.gf('django.contrib.gis.db.models.fields.LineStringField')(default=None))

        # Changing field 'Route.multiline'
        db.alter_column(u'directions_route', 'multiline', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(default=None))

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
            'direction': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True'}),
            'multiline': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True'}),
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