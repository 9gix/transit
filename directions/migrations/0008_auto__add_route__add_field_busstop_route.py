# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table(u'directions_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directions.Bus'])),
            ('multiline', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')()),
            ('line', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
        ))
        db.send_create_signal(u'directions', ['Route'])

        # Adding field 'BusStop.route'
        db.add_column(u'directions_busstop', 'route',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directions.Route'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Route'
        db.delete_table(u'directions_route')

        # Deleting field 'BusStop.route'
        db.delete_column(u'directions_busstop', 'route_id')


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
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directions.Route']", 'null': 'True'}),
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