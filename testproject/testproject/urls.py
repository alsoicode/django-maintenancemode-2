"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from distutils.version import StrictVersion
from django.conf.urls import include
from django.contrib import admin
from maintenancemode.utils.settings import DJANGO_VERSION

if DJANGO_VERSION >= StrictVersion('2.0'): 
    from django.urls import path
    urlpatterns = [
        path(r'admin/', admin.site.urls),
        path(r'', include('app.urls')),
    ]
    
else:
    from django.conf.urls import url
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('app.urls', namespace='app')),
    ]
