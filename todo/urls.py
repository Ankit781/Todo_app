from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', TaskReadAllView.as_view(), name ="task-list"),
    path('tasks/create', TaskCreateView.as_view(), name ="task-create"),
    path('tasks/<int:pk>/', TaskReadOneView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]