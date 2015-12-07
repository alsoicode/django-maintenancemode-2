from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^ignored-page/$', views.ignored, name='ignored'),
    url(r'^$', views.home, name='home'),
]
