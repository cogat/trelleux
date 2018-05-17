# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrelloBoard'
        db.create_table(u'trelleux_trelloboard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_auth_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('board_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fail_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('days_in_future', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
        ))
        db.send_create_signal(u'trelleux', ['TrelloBoard'])


    def backwards(self, orm):
        # Deleting model 'TrelloBoard'
        db.delete_table(u'trelleux_trelloboard')


    models = {
        u'trelleux.trelloboard': {
            'Meta': {'object_name': 'TrelloBoard'},
            'board_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_auth_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'days_in_future': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fail_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {})
        }
    }

    complete_apps = ['trelleux']