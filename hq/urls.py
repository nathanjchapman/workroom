from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^project/add/$', views.project_add, name="project_add"),
    url(r'^address/add/$', views.address_add, name="address_add"),
]
