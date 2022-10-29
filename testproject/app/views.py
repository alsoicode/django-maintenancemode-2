from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class IgnoredView(TemplateView):
    template_name = "ignored.html"
