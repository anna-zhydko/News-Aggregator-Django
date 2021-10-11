from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('task/', views.get_task_info)]
