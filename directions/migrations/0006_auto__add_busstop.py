# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BusStop'
        db.create_table(u'directions_busstop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directions.Bus'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directions.Stop'])),
            ('direction', self.gf('django.db.models.fields.IntegerField')()),
            ('distance', self.gf('django.db.models.fields.FloatField')()),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'directions', ['BusStop'])

        # Removing M2M table for field stops on 'Bus'
        db.delete_table('directions_bus_stops')


    def backwards(self, orm):
        # Deleting model 'BusStop'
        db.delete_table(u'directions_busstop')

        # Adding M2M table for field stops on 'Bus'
        db.create_table(u'directions_bus_stops', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bus', models.ForeignKey(orm[u'directions.bus'], null=False)),
            ('stop', models.ForeignKey(orm[u'directions.stop'], null=False))
        ))
        db.create_unique(u'directions_bus_stops', ['bus_id', 'stop_id'])


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
            'direction': ('django.db.models.fields.IntegerField', [], {}),
            'distance': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
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