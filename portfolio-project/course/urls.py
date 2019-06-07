from django.urls import path, include
from . import views

urlpatterns = [
    path('createcourse', views.createcourse, name='createcourse'),
]
