# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TrelloBoard.board_realid'
        db.add_column(u'trelleux_trelloboard', 'board_realid',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TrelloBoard.board_realid'
        db.delete_column(u'trelleux_trelloboard', 'board_realid')


    models = {
        u'trelleux.trelloboard': {
            'Meta': {'object_name': 'TrelloBoard'},
            'board_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'board_realid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'client_auth_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'days_in_future': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fail_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {})
        }
    }

    complete_apps = ['trelleux']