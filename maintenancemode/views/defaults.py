import json
from django.template import loader, RequestContext

from django import VERSION as DJANGO_VERSION
from maintenancemode.http import HttpResponseTemporaryUnavailable
from maintenancemode.utils.settings import MAINTENANCE_503_TEMPLATE


def temporary_unavailable(request, template_name=MAINTENANCE_503_TEMPLATE):
    """
    Default 503 handler
    """
    # let's be kind to json api calls...
    # NB we specify that we're down for maintenance 
    # so a plain 
    if request.META.get("CONTENT_TYPE") == "application/json":
        content = json.dumps({
                "code": 503,
                "error": "temporarily_unavailable",
                "reason": "maintenance",
                "error_description": "Sorry, the service is temporarily down for maintenance"
                })
        content_type = "application/json"
    else:
        args = [template_name, {'request_path': request.path}]
        if DJANGO_VERSION < (1, 10, 0):
            args.append(RequestContext(request))
        content = loader.render_to_string(*args)
        content_type = "text/html"

    return HttpResponseTemporaryUnavailable(content, content_type=content_type)
