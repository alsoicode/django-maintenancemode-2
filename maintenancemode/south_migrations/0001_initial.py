# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Maintenance'
        db.create_table('maintenancemode_maintenance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('is_being_performed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('maintenancemode', ['Maintenance'])

        # Adding model 'IgnoredURL'
        db.create_table('maintenancemode_ignoredurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('maintenance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maintenancemode.Maintenance'])),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal('maintenancemode', ['IgnoredURL'])


    def backwards(self, orm):

        # Deleting model 'Maintenance'
        db.delete_table('maintenancemode_maintenance')

        # Deleting model 'IgnoredURL'
        db.delete_table('maintenancemode_ignoredurl')


    models = {
        'maintenancemode.ignoredurl': {
            'Meta': {'object_name': 'IgnoredURL'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintenance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maintenancemode.Maintenance']"}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'maintenancemode.maintenance': {
            'Meta': {'object_name': 'Maintenance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_being_performed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['maintenancemode']
