from django.template import Context, loader, RequestContext

from maintenancemode.http import HttpResponseTemporaryUnavailable

def temporary_unavailable(request, template_name='503.html'):
    """
    Default 503 handler, which looks for the requested URL in the redirects
    table, redirects if found, and displays 404 page if not redirected.
    
    Templates: `503.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    return HttpResponseTemporaryUnavailable(loader.render_to_string(template_name, {
        'request_path': request.path,
    }, RequestContext(request)))
