from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.overview, name="overview"),
    path('project/add/', views.project_add, name="project_add"),
    path('project/<int:project_id>/', include([
        path('', views.project_detail, name="project_detail"),
        path('archive/', views.project_archive, name="project_archive"),
        path('delete/', views.project_delete, name="project_delete"),
        ])),
    path('address/add/', views.address_add, name="address_add"),
    path('address/<int:address_id>', include([
        path('', views.address_detail, name="address_detail"),
        path('delete/', views.address_delete, name="address_delete"),
        ])),
]
