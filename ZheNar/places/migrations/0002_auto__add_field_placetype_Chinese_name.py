# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PlaceType.Chinese_name'
        db.add_column(u'places_placetype', 'Chinese_name',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PlaceType.Chinese_name'
        db.delete_column(u'places_placetype', 'Chinese_name')


    models = {
        u'places.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['places.PlaceType']"})
        },
        u'places.placetype': {
            'Chinese_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'PlaceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['places']