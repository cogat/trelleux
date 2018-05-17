# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ClientToken'
        db.delete_table(u'trelleux_clienttoken')

        # Adding model 'TrelloClient'
        db.create_table(u'trelleux_trelloclient', (
            ('client_auth_token', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'trelleux', ['TrelloClient'])


    def backwards(self, orm):
        # Adding model 'ClientToken'
        db.create_table(u'trelleux_clienttoken', (
            ('client_auth_token', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'trelleux', ['ClientToken'])

        # Deleting model 'TrelloClient'
        db.delete_table(u'trelleux_trelloclient')


    models = {
        u'trelleux.trelloclient': {
            'Meta': {'object_name': 'TrelloClient'},
            'client_auth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['trelleux']