from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overveiw"),
    url(r'^timecard/add/$', views.add_timecard, name="add timecard"),
    url(r'^timecards/completed/$', views.completed, name="completed"),
    url(r'^timecard/(?P<timecard_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^timecard/(?P<timecard_id>[0-9]+)/review/$', views.review, name="review"),
    url(r'^timecard/(?P<timecard_id>[0-9]+)/update/$', views.update, name="update"),
    #url(r'^(?P<timecard_id>[0-9]+)/delete/$', views.delete, name="delete"),
]
