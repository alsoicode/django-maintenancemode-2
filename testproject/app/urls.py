from django.urls import re_path

from . import views

app_name = 'app'

urlpatterns = [
    re_path(r'^ignored-page/$', views.IgnoredView.as_view(), name='ignored'),
    re_path(r'^$', views.HomeView.as_view(), name='home'),
]
