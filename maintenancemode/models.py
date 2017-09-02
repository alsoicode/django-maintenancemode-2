from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Maintenance(models.Model):
    site = models.ForeignKey(Site)
    is_being_performed = models.BooleanField(
        _('In Maintenance Mode'), default=False
    )

    class Meta:
        verbose_name = verbose_name_plural = _('Maintenance Mode')

    def __str__(self):
        return self.site.domain


@python_2_unicode_compatible
class IgnoredURL(models.Model):
    maintenance = models.ForeignKey(Maintenance)
    pattern = models.CharField(max_length=255)
    description = models.CharField(
        max_length=75, help_text=_('What this URL pattern covers.')
    )

    def __str__(self):
        return self.pattern
