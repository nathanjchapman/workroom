from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.overview, name="overview"),
    path('door/add/', views.door_add, name="door_add"),
    path('code/add/', views.code_add, name="code_add"),
    path('code/<int:code_id>/', include([
        path('', views.code_detail, name="code_detail"),
        path('delete/', views.code_delete, name="code_delete"),
        ])),
]
