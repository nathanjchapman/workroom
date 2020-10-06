from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.overview, name="overview"),
    path('labor-class/add/', views.labor_class_add, name="labor_class_add"),
    path('labor-group/add/', views.labor_group_add, name="labor_group_add"),
    path('labor-item/add/', views.labor_item_add, name="labor_item_add"),
]
