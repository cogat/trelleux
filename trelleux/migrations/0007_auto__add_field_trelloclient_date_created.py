# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TrelloClient.date_created'
        db.add_column(u'trelleux_trelloclient', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2016, 2, 13, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TrelloClient.date_created'
        db.delete_column(u'trelleux_trelloclient', 'date_created')


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
            'client_auth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['trelleux']