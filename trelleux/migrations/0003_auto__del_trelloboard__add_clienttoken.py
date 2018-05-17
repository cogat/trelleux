# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TrelloBoard'
        db.delete_table(u'trelleux_trelloboard')

        # Adding model 'ClientToken'
        db.create_table(u'trelleux_clienttoken', (
            ('client_auth_token', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'trelleux', ['ClientToken'])


    def backwards(self, orm):
        # Adding model 'TrelloBoard'
        db.create_table(u'trelleux_trelloboard', (
            ('board_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('client_auth_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fail_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('days_in_future', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('board_realid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')()),
        ))
        db.send_create_signal(u'trelleux', ['TrelloBoard'])

        # Deleting model 'ClientToken'
        db.delete_table(u'trelleux_clienttoken')


    models = {
        u'trelleux.clienttoken': {
            'Meta': {'object_name': 'ClientToken'},
            'client_auth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['trelleux']