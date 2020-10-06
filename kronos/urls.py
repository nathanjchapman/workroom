from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.overview, name="overview"),
    path('add/', views.timecard_add, name="timecard_add"),
    path('complete/', views.timecard_complete_index, name="timecard_complete_index"),
    path('timecards/', views.timecard_index, name="timecard_index"),
    path('<int:timecard_id>/', include([
        path('', views.timecard_detail, name="timecard_detail"),
        path('complete/', views.timecard_complete, name="timecard_complete"),
        path('review/', views.timecard_review, name="timecard_review"),
        path('update/', views.timecard_update, name="timecard_update"),
        path('delete/', views.timecard_delete, name="timecard_delete"),
        path('task/add/', views.task_add, name="task_add"),
        path('task/<int:task_id>/', include([
            path('', views.task_detail, name="task_detail"),
            path('update/', views.task_update, name="task_update"),
            path('copy/', views.task_copy, name="task_copy"),
            path('delete/', views.task_delete, name="task_delete"),
        ])),
    ])),
]
