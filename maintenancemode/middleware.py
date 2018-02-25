import re
from distutils.version import StrictVersion

import django.conf.urls as urls
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import resolvers
from django.utils import deprecation

from maintenancemode.models import Maintenance
from maintenancemode.utils.settings import (
    DJANGO_VERSION, MAINTENANCE_ADMIN_IGNORED_URLS, MAINTENANCE_BLOCK_STAFF)

urls.handler503 = 'maintenancemode.views.defaults.temporary_unavailable'
urls.__all__.append('handler503')

_base = deprecation.MiddlewareMixin if DJANGO_VERSION >= StrictVersion('1.10.0') else object


class MaintenanceModeMiddleware(_base):
    def process_request(self, request):
        """
        Check if the current site is in maintenance.
        """

        # First check things that don't require a database access:

        # Allow access if remote ip is in INTERNAL_IPS
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return None

        # Check if the staff the user is allowed
        if hasattr(request, 'user'):
            if request.user.is_superuser:
                return None

            if not MAINTENANCE_BLOCK_STAFF and request.user.is_staff:
                return None

        # ok let's look at the db
        site = Site.objects.get_current()
        try:
            maintenance = Maintenance.objects.get(site=site)
        except Maintenance.DoesNotExist:
            # Allow access if no matching Maintenance object exists
            return None

        # Allow access if maintenance is not being performed
        if not maintenance.is_being_performed:
            return None

        # Check if a path is explicitly excluded from maintenance mode
        ignored_url_list = set(
            maintenance.ignored_url_patterns() + MAINTENANCE_ADMIN_IGNORED_URLS
        )

        ignored_url_patterns = tuple(
            re.compile(r'{}'.format(url)) for url in ignored_url_list
        )

        request_path = request.path_info.lstrip("/")

        for url in ignored_url_patterns:
            if url.match(request_path):
                return None

        # Otherwise show the user the 503 page
        resolver = resolvers.get_resolver(None)

        resolve = resolver.resolve_error_handler
        callback, param_dict = resolve('503')
        return callback(request, **param_dict)
