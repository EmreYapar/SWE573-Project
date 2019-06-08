from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('createcourse', views.createcourse, name='createcourse'),
    path('wikidata', views.wikidata, name='wikidata'),
]
