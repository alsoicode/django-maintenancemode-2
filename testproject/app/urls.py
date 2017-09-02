from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^ignored-page/$',
        view=views.IgnoredView.as_view(),
        name='ignored'
    ),
    url(
        regex=r'^$',
        view=views.HomeView.as_view(),
        name='home'
    ),
]
