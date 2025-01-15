from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('tasks/',TaskView.as_view(),name='tasks_list'),
    path('tasks/<int:task_id>/', TaskView.as_view(),name='task_detail'), 
]
