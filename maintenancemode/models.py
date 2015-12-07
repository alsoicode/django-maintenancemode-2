from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
from django.template.defaultfilters import join


class Maintenance(models.Model):
    site = models.ForeignKey(Site)
    is_being_performed = models.BooleanField('In Maintenance Mode', default=False)

    class Meta:
        verbose_name = verbose_name_plural = 'Maintenance Mode'

    def __unicode__(self):
        return self.site.domain

class IgnoredURL(models.Model):
    maintenance = models.ForeignKey(Maintenance)
    pattern = models.CharField(max_length=255)
    description = models.CharField(max_length=75, help_text='What this URL pattern covers.')

    def __unicode__(self):
        return self.pattern
