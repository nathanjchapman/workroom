from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overveiw, name="overveiw"),
    url(r'^add', views.add_timecard, name="add timecard"),
    url(r'^(?P<timecard_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^(?P<timecard_id>[0-9]+)/review/$', views.review, name="review"),
    url(r'^(?P<timecard_id>[0-9]+)/edit/$', views.edit, name="edit"),
    url(r'^(?P<timecard_id>[0-9]+)/delete/$', views.delete, name="delete"),
]
