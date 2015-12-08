try:
    import httplib
except ImportError:
    import http.client as httplib

import os.path
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.template import TemplateDoesNotExist

from maintenancemode import middleware as mw
from maintenancemode.models import Maintenance, IgnoredURL
from maintenancemode.utils.settings import DJANGO_MINOR_VERSION

from .urls import urlpatterns


class MaintenanceModeMiddlewareTestCase(TestCase):
    def setUp(self):
        # Reset config options adapted in the individual tests

        mw.MAINTENANCE_MODE = False
        # settings.INTERNAL_IPS = ()

        # Site
        site = Site.objects.get_current()
        self.maintenance, _ = Maintenance.objects.get_or_create(site=site)

        # User
        self.username = 'maintenance'
        self.password = 'maintenance_pw'

        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=self.username,
                email='maintenance@example.org', password=self.password)

        self.user = user

        # urls
        self.home_url = reverse('app:home')
        self.ignored_url = reverse('app:ignored')

        # Text checks
        self.home_page_text = 'This is the home view.'
        self.maintenance_page_text = 'Temporarily unavailable'

    def turn_maintenance_mode_on(self):
        self.maintenance.is_being_performed = True
        self.maintenance.save()

    def turn_maintenance_mode_off(self):
        maintenance = Maintenance.objects.get(site=self.site)
        self.maintenance.is_being_performed = False
        self.maintenance.save()

    def test_implicitly_disabled_middleware(self):
        # Middleware should default to being disabled

        response = self.client.get(self.home_url)
        self.assertContains(response, text=self.home_page_text, count=1,
            status_code=200)

    def test_disabled_middleware(self):
        # Explicitly disabling the MAINTENANCE_MODE should work as expected
        mw.MAINTENANCE_MODE = False

        response = self.client.get(self.home_url)
        self.assertContains(response, text=self.home_page_text, count=1,
            status_code=200)

    def test_enabled_middleware_without_template(self):
        """
        Enabling the middleware without a proper 503 template should raise a
        template error
        """
        if DJANGO_MINOR_VERSION > 7:
            templates_override = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [],
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    },
                },
            ]

            with self.settings(TEMPLATES=templates_override):
                mw.MAINTENANCE_MODE = True

                self.assertRaises(TemplateDoesNotExist, self.client.get, self.home_url)

        else:
            with self.settings(TEMPLATE_DIRS=()):
                mw.MAINTENANCE_MODE = True

                self.assertRaises(TemplateDoesNotExist, self.client.get, self.home_url)

    def test_enabled_middleware_with_template(self):
        """
        Enabling the middleware having a 503.html in any of the template locations
        should return the rendered template
        """

        self.turn_maintenance_mode_on()

        # reset INTERNAL_IPS so that the request will appear to come from the outside
        with self.settings(INTERNAL_IPS=()):
            response = self.client.get(self.home_url)
            self.assertContains(response, text=self.maintenance_page_text, count=1,
                status_code=503)

    def test_middleware_with_non_staff_user(self):
        """
        A logged in user that is not a staff user should see the 503 message
        """

        self.turn_maintenance_mode_on()

        self.client.login(username=self.username, password=self.password)

        with self.settings(INTERNAL_IPS=()):
            response = self.client.get(self.home_url)
            self.assertContains(response, text=self.maintenance_page_text, count=1,
                status_code=503)

    def test_middleware_with_staff_user(self):
        """
        A logged in user that _is_ a staff user should be able to use the site normally
        """

        self.user.is_staff = True
        self.user.save()

        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.home_url)
        self.assertContains(response, text=self.home_page_text, count=1,
            status_code=200)

    def test_middleware_with_internal_ips(self):
        """
        A user that visits the site from an IP in INTERNAL_IPS should be able to use the site normally
        """

        self.turn_maintenance_mode_on()

        # Use a new Client instance to be able to set the REMOTE_ADDR used by INTERNAL_IPS
        client = Client(REMOTE_ADDR='127.0.0.1')

        with self.settings(INTERNAL_IPS=('127.0.0.1',)):
            response = client.get(self.home_url)
            self.assertContains(response, text=self.home_page_text, count=1, status_code=200)

    def test_ignored_path(self):
        """
        A path is ignored when applying the maintanance mode and should be reachable normally
        """

        self.turn_maintenance_mode_on()

        # Add a pattern to ignore
        maintenance = Maintenance.objects.all()[0]
        IgnoredURL.objects.get_or_create(maintenance=maintenance,
            pattern=urlpatterns[0].regex.pattern)  # r'^ignored-page/$'

        response = self.client.get(self.ignored_url)
        self.assertContains(response, text='Ignored', count=1, status_code=200)

    def test_django_admin_accessable(self):
        """
        Make sure we can still log into Django admin to turn maintenance mode off
        """

        self.turn_maintenance_mode_on()
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, httplib.OK, 'Unable to reach Django Admin login')
