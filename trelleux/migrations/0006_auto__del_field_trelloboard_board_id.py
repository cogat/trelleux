# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TrelloBoard.board_id'
        db.delete_column(u'trelleux_trelloboard', 'board_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'TrelloBoard.board_id'
        raise RuntimeError("Cannot reverse this migration. 'TrelloBoard.board_id' and its values cannot be restored.")

    models = {
        u'trelleux.trelloboard': {
            'Meta': {'object_name': 'TrelloBoard'},
            'board_realid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'boards'", 'to': u"orm['trelleux.TrelloClient']"}),
            'days_in_future': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fail_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {})
        },
        u'trelleux.trelloclient': {
            'Meta': {'object_name': 'TrelloClient'},
            'client_auth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['trelleux']