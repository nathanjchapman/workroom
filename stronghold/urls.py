from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.overview, name="overview"),
    url(r'^door/add/$', views.door_add, name="door_add"),
    url(r'^code/add/$', views.code_add, name="code_add"),
    url(r'^code/(?P<code_id>[0-9]+)/', include([
        url(r'^$', views.code_detail, name="code_detail"),
        ])),
]
