from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.contrib.sites.models import Site


@python_2_unicode_compatible
class Maintenance(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    is_being_performed = models.BooleanField(
        _('In Maintenance Mode'), default=False
    )

    class Meta:
        verbose_name = verbose_name_plural = _('Maintenance Mode')

    def __str__(self):
        return self.site.domain

    def ignored_url_patterns(self):
        qs = self.ignoredurl_set.values_list(
            "pattern", flat=True
            )
        return list(qs)


@python_2_unicode_compatible
class IgnoredURL(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    pattern = models.CharField(max_length=255)
    description = models.CharField(
        max_length=75, help_text=_('What this URL pattern covers.')
    )

    def __str__(self):
        return self.pattern


def populate():
    """
    creates Maintenance objects for all sites (if necessary)
    """
    for site in Site.objects.all():
        try:
            Maintenance.objects.get_or_create(site=site)
        except IntegrityError as e:
            # MySQL can be a bit annoying sometimes
            pass

