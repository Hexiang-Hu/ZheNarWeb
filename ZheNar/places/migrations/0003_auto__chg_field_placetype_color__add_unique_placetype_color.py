# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PlaceType.color'
        db.alter_column(u'places_placetype', 'color', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10))
        # Adding unique constraint on 'PlaceType', fields ['color']
        db.create_unique(u'places_placetype', ['color'])


    def backwards(self, orm):
        # Removing unique constraint on 'PlaceType', fields ['color']
        db.delete_unique(u'places_placetype', ['color'])


        # Changing field 'PlaceType.color'
        db.alter_column(u'places_placetype', 'color', self.gf('django.db.models.fields.SmallIntegerField')())

    models = {
        u'places.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'create_time': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['places.PlaceType']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'places.placetype': {
            'Meta': {'object_name': 'PlaceType'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'Red'", 'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['places']