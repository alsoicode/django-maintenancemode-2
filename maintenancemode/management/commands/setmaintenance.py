# -*- coding: utf-8 -*-
from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.contrib.sites.models import Site
from maintenancemode.models import Maintenance


class Command(BaseCommand):
    help = (
        "Set maintenance-mode on or off for <site_id>."
        " If no site_id given, will use settings.SITE_ID"
    )

    args = "status [site_id [site_id]*]"

    status_map = {"on": True, "off": False}
    status_rmap = {v: k for k, v in status_map.items()}

    if DJANGO_VERSION >= (1, 8, 0):
        def add_arguments(self, parser):
            parser.add_argument(
                "status",
                choices=("on", "off"),
                help="<status> (on/off)"
            )

            parser.add_argument(
                "args",
                nargs="*",
                type=int,
                help="<site_id>*"
            )

            parser.add_argument(
                "-i", "--ignore-missing",
                action="store_true",
                # type=bool,
                default=False,
                help="ignore any inexistant site_id (default %(default)s)"
            )

    else:
        # pre 1.8 compat using optparse
        # here we have to manually get
        # `status` from `*args` and set it as
        # `options['status']`
        from optparse import make_option

        option_list = BaseCommand.option_list + (
            make_option(
                "-i", "--ignore-missing",
                action="store_true",
                # type=bool,
                default=False,
                help="ignore any inexistant site_id (default False)"
            )
        )

    def _compat_parse_args(self, args, options):
        if DJANGO_VERSION < (1, 8, 0):
            try:
                status, args = args[0], args[1:]
            except IndexError:
                raise CommandError("missing <status> (on / off) argument")
            if status not in self.status_map:
                raise CommandError(
                    "invalid <status> argument '{}'"
                    " (should be either 'on' or 'off')".format(status)
                )
            options["status"] = status

        return args, options

    def handle(self, *args, **options):
        args, options = self._compat_parse_args(args, options)

        # print "args : {}".format(args)
        # print "options : {}".format(options)

        site_ids = args or (settings.SITE_ID, )
        known_sites = Site.objects.all()
        missings = \
            set(site_ids) - set(known_sites.values_list("id", flat=True))

        if missings and not options["ignore_missing"]:
            raise CommandError(
                "Unknown site ids: {}".format(" ".join(map(str, missings)))
            )

        status = self.status_map[options["status"]]
        for site_id in site_ids:
            # handle the case of --ignore-missing
            if site_id in missings:
                if options["verbosity"] >= 1:
                    self.stderr.write(
                        "unknown site {} - skipping\n".format(site_id)
                    )
                    continue

            m, created = Maintenance.objects.get_or_create(site_id=site_id)

            if m.is_being_performed == status:
                if options["verbosity"] >= 1:
                    self.stderr.write(
                        "Site {site_id} ({site}) already {status}\n".format(
                            site_id=site_id,
                            site=m.site,
                            status=self.status_rmap[status]
                        )
                    )
                continue

            m.is_being_performed = status
            m.save()
            if options["verbosity"] >= 1:
                self.stderr.write(
                    "Site {site_id} ({site}) is now {status}\n".format(
                        site_id=site_id,
                        site=m.site,
                        status=self.status_rmap[status]
                    )
                )
