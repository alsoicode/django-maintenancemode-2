from django.template import Context, loader, RequestContext

from django import VERSION as DJANGO_VERSION
from maintenancemode.http import HttpResponseTemporaryUnavailable
from maintenancemode.utils.settings import MAINTENANCE_503_TEMPLATE


def temporary_unavailable(request, template_name=MAINTENANCE_503_TEMPLATE):
    """
    Default 503 handler, which looks for the requested URL in the redirects
    table, redirects if found, and displays 404 page if not redirected.

    """
    if DJANGO_VERSION >= (1, 10, 0):
	    return HttpResponseTemporaryUnavailable(loader.render_to_string(template_name, {'request_path': request.path,}))
    else:		
        return HttpResponseTemporaryUnavailable(loader.render_to_string(template_name, {
            'request_path': request.path,
        }, RequestContext(request)))
