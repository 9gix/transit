# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bus'
        db.create_table(u'directions_bus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('no', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('direction', self.gf('django.db.models.fields.IntegerField')()),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'directions', ['Bus'])

        # Adding M2M table for field stops on 'Bus'
        db.create_table(u'directions_bus_stops', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bus', models.ForeignKey(orm[u'directions.bus'], null=False)),
            ('stop', models.ForeignKey(orm[u'directions.stop'], null=False))
        ))
        db.create_unique(u'directions_bus_stops', ['bus_id', 'stop_id'])

        # Adding model 'Stop'
        db.create_table(u'directions_stop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'directions', ['Stop'])


    def backwards(self, orm):
        # Deleting model 'Bus'
        db.delete_table(u'directions_bus')

        # Removing M2M table for field stops on 'Bus'
        db.delete_table('directions_bus_stops')

        # Deleting model 'Stop'
        db.delete_table(u'directions_stop')


    models = {
        u'directions.bus': {
            'Meta': {'object_name': 'Bus'},
            'direction': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directions.Stop']", 'symmetrical': 'False'})
        },
        u'directions.stop': {
            'Meta': {'object_name': 'Stop'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['directions']