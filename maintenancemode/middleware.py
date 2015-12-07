import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db.utils import DatabaseError
import django.conf.urls as urls

from maintenancemode.models import Maintenance, IgnoredURL
from maintenancemode.utils.settings import DJANGO_MINOR_VERSION

urls.handler503 = 'maintenancemode.views.defaults.temporary_unavailable'
urls.__all__.append('handler503')


class MaintenanceModeMiddleware(object):
    def process_request(self, request):
        """
        Get the maintenance mode from the database.
        If a Maintenance value doesn't already exist in the database, we'll create one.
        "has_add_permission" and "has_delete_permission" are overridden in admin
        to prevent the user from adding or deleting a record, as we only need one
        to affect multiple sites managed from one instance of Django admin.
        """
        site = Site.objects.get_current()

        try:
            maintenance = Maintenance.objects.get(site=site)
        except (Maintenance.DoesNotExist, DatabaseError):
            for site in Site.objects.all():
                maintenance = Maintenance.objects.create(site=site, is_being_performed=False)

        # Allow access if maintenance is not being performed
        if not maintenance.is_being_performed:
            return None

        # Allow access if remote ip is in INTERNAL_IPS
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return None

        # Allow access if the user doing the request is logged in and a
        # staff member.
        if hasattr(request, 'user') and request.user.is_staff:
            return None

        # Check if a path is explicitly excluded from maintenance mode
        urls_to_ignore = IgnoredURL.objects.filter(maintenance=maintenance)
        ignore_urls = tuple([re.compile(r'%s' % str(url.pattern)) for url in urls_to_ignore])
        request_path = request.path_info[1:]
        for url in ignore_urls:
            if url.match(request_path):
                return None

        # Otherwise show the user the 503 page
        resolver = urlresolvers.get_resolver(None)

        if DJANGO_MINOR_VERSION < 8:
            callback, param_dict = resolver._resolve_special('503')
        else:
            callback, param_dict = resolver.resolve_error_handler('503')

        return callback(request, **param_dict)
