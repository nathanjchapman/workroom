from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overview"),
    url(r'^labor-class/add/$', views.labor_class_add, name="labor_class_add"),
    url(r'^labor-group/add/$', views.labor_group_add, name="labor_group_add"),
    url(r'^labor-item/add/$', views.labor_item_add, name="labor_item_add"),
]
