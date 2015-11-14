from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overview"),
    url(r'^project/add/$', views.project_add, name="project_add"),
    url(r'^project/(?P<code_id>[0-9]+)/', include([
        url(r'^$', views.project_detail, name="project_detail"),
        ])),
    url(r'^address/add/$', views.address_add, name="address_add"),
    url(r'^address/(?P<code_id>[0-9]+)/', include([
        url(r'^$', views.address_detail, name="address_detail"),
        ])),
]
