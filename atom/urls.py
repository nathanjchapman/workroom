from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overview"),
    url(r'^li_class/add/$', views.li_class_add, name="li_class_add"),
    url(r'^li_number/add/$', views.li_number_add, name="li_number_add"),
]
