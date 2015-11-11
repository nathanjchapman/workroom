from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^project/add/$', views.addproject, name="addproject"),
]
