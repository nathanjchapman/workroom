from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overview"),
    url(r'^add/$', views.add_timecard, name="add timecard"),
    url(r'^complete/$', views.complete, name="complete"),
    url(r'^timecards/$', views.timecards, name="timecards"),
    url(r'^(?P<timecard_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^(?P<timecard_id>[0-9]+)/review/$', views.review, name="review"),
    url(r'^(?P<timecard_id>[0-9]+)/update/$', views.update, name="update"),
    url(r'^(?P<timecard_id>[0-9]+)/delete/$', views.deletetc, name="deletetc"),
    url(r'^(?P<timecard_id>[0-9]+)/task/add/$', views.add_task, name="addtask"),
    url(r'^(?P<timecard_id>[0-9]+)/task/(?P<task_id>[0-9]+)/$', views.detail_task, name="detail_task"),
    url(r'^(?P<timecard_id>[0-9]+)/task/(?P<task_id>[0-9]+)/delete/$', views.delete_task, name="delete_task"),
]
