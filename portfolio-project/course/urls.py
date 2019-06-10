from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('createcourse', views.createcourse, name='createcourse'),
    path('wikidata', views.wikidata, name='wikidata'),
    path('summernote/', include('django_summernote.urls')),
    path('createcoursepart', views.createcoursepart, name='createcoursepart'),
    path('createquiz', views.createquiz, name='createquiz'),
    path('<int:course_id>', views.viewcourse, name='viewcourse'),
    path('viewcourseparts', views.viewcourseparts, name='viewcourseparts'),
    path('viewcoursequiz', views.viewcoursequiz, name='viewcoursequiz'),
]
