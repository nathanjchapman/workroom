from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overview"),
    url(r'^add/$', views.timecard_add, name="timecard_add"),
    url(r'^complete/$', views.timecard_complete, name="timecard_complete"),
    url(r'^timecards/$', views.timecard_index, name="timecard_index"),
    url(r'^(?P<timecard_id>[0-9]+)/', include([
        url(r'^$', views.timecard_detail, name="timecard_detail"),
        url(r'^review/$', views.timecard_review, name="timecard_review"),
        url(r'^update/$', views.timecard_update, name="timecard_update"),
        url(r'^delete/$', views.timecard_delete, name="timecard_delete"),
        url(r'^task/add/$', views.task_add, name="task_add"),
        url(r'^task/(?P<task_id>[0-9]+)/', include([
            url(r'^$', views.task_detail, name="task_detail"),
            url(r'^delete/$', views.task_delete, name="task_delete"),
        ])),
    ])),
]
